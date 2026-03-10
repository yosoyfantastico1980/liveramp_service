from dotenv import load_dotenv
load_dotenv()

# ==============================
# Standard Library
# ==============================
import os
import time
import json
import ssl
import uuid
import logging
import urllib.parse
import urllib.request
import urllib.error
import base64


from typing import Any, Dict, List, Optional, Tuple, Union, Annotated
from enum import Enum
from models.pricing_segment import BulkReconciliationRequest
from models.segment_updates import SegmentUpdatesResponse
from models.pricing_segment import PriceChangeResponse

from itertools import groupby
from collections import defaultdict
from datetime import datetime, date


import certifi
import csv
from io import StringIO
from fastapi.responses import StreamingResponse

# ==============================
# FastAPI
# ==============================
from fastapi import (
    FastAPI,
    APIRouter,
    Header,
    HTTPException,
    Depends,
    Query,
    Body,
    Request,
    Security,
)

from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKeyHeader
from fastapi.openapi.utils import get_openapi

from app.config import settings

# ==============================
# Local Models
# ==============================
from models.liveramp import (
    DestinationListResponse,
    SegmentListResponse,
    MarketplaceSegmentListResponse,
    MarketplaceSegmentDetailResponse,
    RequestedSegmentsRequest,
    RequestedSegmentsResponse,
    SegmentStatusListResponse,
    DeliveryListResponse,
    FirstPartyDistributionRequest,      # ✅ ADD
    FirstPartyDistributionResponse,     # ✅ ADD
    IdentifierType,
    CountryCode,
    CurrencyCode,
    SegmentType,
    SegmentPricingHistoryResponse,
    SegmentPricingRecord,
    PricingSource
)

# ==============================
# Adapters
# ==============================
from app.services.liveramp_adapter import (
    map_destinations_response,
    map_segments_response,
    map_marketplace_segments_response,
    map_requested_segments_request,
    map_requested_segments_response,
    map_segment_statuses_response,
    map_marketplace_segment_detail_response,
    map_deliveries_response,
    map_first_party_distribution_request,    # ✅ ADD
    map_first_party_distribution_response,   # ✅ ADD
)


from app.services.pricing_service import PricingService
import inspect
print("LOADED PricingService FROM:", inspect.getfile(PricingService))


from pydantic import BaseModel
from typing import List


# ==========================
# Internal Pricing Models
# ==========================


class PricingStatus(str, Enum):
    unpriced = "UNPRICED"
    priced = "PRICED"


class PricingHistoryItem(BaseModel):
    price: float
    effective_at: datetime
    source: str


class SegmentPricingResponse(BaseModel):
    segment_id: str
    original_price: float
    current_price: float
    currency: str
    pricing_history: List[PricingHistoryItem]



# ----------------------------
# Logging
# ----------------------------
logger = logging.getLogger("liveramp_service")
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))


# ----------------------------
# App
# ----------------------------
app = FastAPI(
    title="PulsePoint LiveRamp Service",
    version="1.0.0",
description="""
Internal API abstraction layer over LiveRamp Activation and Distribution APIs.

This service provides a standardized and normalized interface for:

- Marketplace segment discovery and activation
- First-party segment distribution
- Unified activation status monitoring
- Destination discovery and delivery tracking

----------------------------------------

Organization Scoping

All endpoints are automatically scoped to the configured LiveRamp organization.

The organization ID is:
- Automatically resolved server-side
- Not caller-configurable
- Not exposed via request headers

This ensures consistent activation behavior and prevents cross-org misuse.

----------------------------------------

This service is intended for internal PulsePoint platform usage.
""",
    openapi_version="3.0.3",
    openapi_tags=[
        {
            "name": "System",
            "description": "Service health and readiness endpoints",
        },
       
        {
            "name": "Destination & Delivery",
            "description": "Destination discovery and segment delivery monitoring"
        },       
        {
            "name": "1st Party Data",
            "description": "First-party segment management and distribution via LiveRamp Distribution API"
        },
        {
            "name": "3rd Party Marketplace",
            "description": "Marketplace segment discovery, details, and activation via LiveRamp Activation API",
        },
        {
            "name": "Activation Monitoring",
            "description": "Activation status tracking and delivery monitoring across both Marketplace and First-Party segments",
        },
    ],
)


# ----------------------------
# Request ID middleware
# ----------------------------
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    rid = request.headers.get("X-Request-Id") or str(uuid.uuid4())
    request.state.request_id = rid
    response = await call_next(request)
    response.headers["X-Request-Id"] = rid
    return response


# ----------------------------
# PulsePoint-facing auth (optional)
# OpenAPI-friendly API key scheme ("Authorize" in Swagger UI)
# ----------------------------
pp_api_key_scheme = APIKeyHeader(name="X-PP-API-Key", auto_error=False)


def require_pp_api_key_security(api_key: Optional[str] = Security(pp_api_key_scheme)) -> None:
    """
    If PP_API_KEY is set in env, require callers to send X-PP-API-Key matching it.
    If PP_API_KEY is NOT set, allow calls (useful for local dev).
    """
    expected = os.getenv("PP_API_KEY")
    if not expected:
        return  # dev mode
    if not api_key or api_key != expected:
        raise HTTPException(status_code=401, detail="Missing/invalid X-PP-API-Key")


# ----------------------------
# SSL context (certifi)
# ----------------------------
def ssl_context() -> ssl.SSLContext:
    # Uses certifi CA bundle to avoid CERTIFICATE_VERIFY_FAILED on corporate networks.
    return ssl.create_default_context(cafile=certifi.where())


# ----------------------------
# LiveRamp token manager (internal only)
# ----------------------------
class TokenManager:
    def __init__(self) -> None:
        self._token: Optional[str] = None
        self._expires_at_epoch: float = 0.0

    def _fetch_new_token(self) -> Dict[str, Any]:
        url = "https://serviceaccounts.liveramp.com/authn/v1/oauth2/token"

        username = os.getenv("LR_CLIENT_ID")
        password = os.getenv("LR_CLIENT_SECRET")

        if not username or not password:
            raise HTTPException(
                status_code=500,
                detail="Missing LR_CLIENT_ID or LR_CLIENT_SECRET",
            )

        form = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_id": "liveramp-api",
        }

        data = urllib.parse.urlencode(form).encode("utf-8")

        req = urllib.request.Request(
            url=url,
            data=data,
            method="POST",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=30, context=ssl_context()) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body)
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Token request failed: {e}")

    def get_access_token(self) -> str:
        now = time.time()

        if self._token and now < (self._expires_at_epoch - 60):
            return self._token

        token_payload = self._fetch_new_token()
        print("TOKEN PAYLOAD:", token_payload)

        access_token = token_payload.get("access_token")
        expires_in = token_payload.get("expires_in", 3600)

        if not access_token:
            raise HTTPException(
                status_code=502,
                detail=f"Token response missing access_token: {token_payload}",
            )

        self._token = access_token
        self._expires_at_epoch = now + float(expires_in)
        return self._token

token_mgr = TokenManager()


# ----------------------------
# LiveRamp org helpers
# ----------------------------
def parse_allowlist() -> Optional[set]:
    allow = os.getenv("LR_ORG_ID_ALLOWLIST", "").strip()
    if not allow:
        return None
    return {x.strip() for x in allow.split(",") if x.strip()}


def resolve_org_id(x_lr_org_id: Optional[str]) -> str:
    """
    Org resolution:
      1) If caller provides X-LR-Org-Id, allow it only if allowlist is set and contains it.
      2) Otherwise fall back to DEFAULT_LR_ORG_ID env var.
    """
    default_org = os.getenv("DEFAULT_LR_ORG_ID")
    allowlist = parse_allowlist()

    if x_lr_org_id:
        if allowlist is not None and x_lr_org_id not in allowlist:
            raise HTTPException(status_code=403, detail="X-LR-Org-Id not allowed")
        return x_lr_org_id

    if not default_org:
        raise HTTPException(
            status_code=500,
            detail="Server is missing DEFAULT_LR_ORG_ID env var",
        )

    return default_org

# ----------------------------
# Startup / readiness helpers
# ----------------------------
def require_env(*names: str) -> None:
    missing = [n for n in names if not os.getenv(n)]
    if missing:
        raise HTTPException(
            status_code=500,
            detail=f"Missing required env vars: {', '.join(missing)}",
        )


def is_truthy(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "y", "on"}


@app.on_event("startup")
def validate_startup_config() -> None:
    """
    Fail-fast startup validation (optional, controlled by env flags).

    Recommended for prod:
      FAIL_FAST_STARTUP=true
      VALIDATE_LR_TOKEN_ON_STARTUP=true
    """
    if not is_truthy("FAIL_FAST_STARTUP"):
        return

    require_env("LR_USERNAME", "LR_PASSWORD", "LR_ORG_ID")

    if is_truthy("REQUIRE_PP_API_KEY") and not os.getenv("PP_API_KEY"):
        raise RuntimeError("REQUIRE_PP_API_KEY is enabled but PP_API_KEY is not set")

    if is_truthy("VALIDATE_LR_TOKEN_ON_STARTUP"):
        _ = token_mgr.get_access_token()


# ----------------------------
# LiveRamp HTTP helpers
# ----------------------------
LR_API_BASE = "https://api.liveramp.com"


def _encode_query(params: List[Tuple[str, Union[str, int]]]) -> str:
    # Keep repeated keys (including keys like countryCodes[]).
    return urllib.parse.urlencode(params, doseq=True)


def lr_request(
    method: str,
    path: str,
    org_id: str,
    query_params: Optional[List[Tuple[str, Union[str, int]]]] = None,
    json_body: Optional[Any] = None,
) -> Any:
    """
    Calls LiveRamp with required headers:
      - Authorization: Bearer <access_token>
      - LR-Org-Id
    Logs upstream status + latency.
    """
    token = token_mgr.get_access_token()
    
    print("REQUEST URL:", LR_API_BASE + path)
    print("TOKEN VALUE:", token)

    url = LR_API_BASE + path
    if query_params:
        url += "?" + _encode_query(query_params)

    headers: Dict[str, str] = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
        "LR-Org-Id": org_id,
    }

    data = None
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(
        url=url,
        data=data,
        method=method.upper(),
        headers=headers,
    )

    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=45, context=ssl_context()) as resp:
            ms = int((time.time() - start) * 1000)
            logger.info(
                "liveramp_upstream_ok method=%s path=%s status=%s ms=%s",
                method.upper(),
                path,
                getattr(resp, "status", None),
                ms,
            )

            raw = resp.read().decode("utf-8")
            if not raw:
                return None
            return json.loads(raw)

    except urllib.error.HTTPError as e:
        ms = int((time.time() - start) * 1000)
        raw = e.read().decode("utf-8") if e.fp else ""
        logger.warning(
            "liveramp_upstream_error method=%s path=%s status=%s ms=%s body=%s",
            method.upper(),
            path,
            e.code,
            ms,
            raw[:500],
        )
        raise HTTPException(
            status_code=502,
            detail=f"LiveRamp {method.upper()} failed: {e.code} {raw}",
        )

    except Exception as e:
        ms = int((time.time() - start) * 1000)
        logger.exception(
            "liveramp_upstream_exception method=%s path=%s ms=%s err=%s",
            method.upper(),
            path,
            ms,
            str(e),
        )
        raise HTTPException(status_code=502, detail=f"LiveRamp {method.upper()} failed: {e}")


# ----------------------------
# Consistent error responses
# ----------------------------
@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"status": exc.status_code, "message": exc.detail}},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": {"status": 500, "message": f"Unhandled server error: {exc}"}},
    )


# ----------------------------
# Versioned router (/v1) - PUBLIC health/ready
# ----------------------------
v1 = APIRouter(prefix="/v1")

pricing_service = PricingService()   # 👈 ADD HERE
print("AVAILABLE METHODS:", dir(pricing_service))


# Dynamic provider enum built from DB at startup
def get_provider_enum():
    cursor = pricing_service.conn.cursor()
    cursor.execute("""
        SELECT DISTINCT p.providername
        FROM portal.dbo.advpixel a
        JOIN portal.dbo.segmentdataprovider p ON a.dataproviderid = p.id
        WHERE a.liverampcustom = true AND a.isactive = true
        ORDER BY p.providername
    """)
    providers = [row[0] for row in cursor.fetchall()]
    return Enum("ProviderName", {p: p for p in providers}, type=str)

ProviderName = get_provider_enum()


@v1.get(
    "/health",
    tags=["System"],
    summary="Health Check",
)
def health():
    return {"status": "ok"}


@v1.get(
    "/ready",
    tags=["System"],
    summary="Readiness Check",
    description="Checks whether the service is ready to process LiveRamp requests.",
)
def ready():
    return {
        "status": "ready",
        "org_id": settings.LIVERAMP_ORG_ID
    }


    """
    Dependency-aware readiness check.
    - Verifies required env/config is present
    - Verifies we can fetch a LiveRamp OAuth token
    - Verifies LiveRamp API connectivity with a lightweight call
    """
    require_env("LR_USERNAME", "LR_PASSWORD", "LR_ORG_ID")

    token = token_mgr.get_access_token()
    if not token:
        raise HTTPException(status_code=500, detail="LiveRamp token is empty")

    org_id = resolve_org_id(x_lr_org_id)
    _ = lr_request("GET", "/activation/v2/destinations", org_id, query_params=[("limit", 10)])

    return {
        "status": "ready",
        "checks": {"env": "ok", "token": "ok", "liveramp_api": "ok"},
    }

@v1.get(
    "/pricing/segments/{segment_id}/history",
    tags=["Pricing"],
    summary="Pricing History (LiveRamp + Hive)",
    description="""
Returns historical pricing timeline for a segment.

Includes:
• LiveRamp original ingestion price  
• PulsePoint Hive overrides  

Does NOT include LIFE reconciliation logic.
Use /reconciliation endpoint for billing validation.
""",
)
def get_pricing_segment_history(segment_id: str):
    org_id = resolve_org_id(None)
    return pricing_service.get_pricing_history(segment_id, org_id)

@v1.get(
    "/pricing/segments/{segment_id}/reconciliation",
    tags=["Pricing"],
    summary="Full Pricing Reconciliation Across Systems",
    description="""
Returns full cross-system pricing audit:

• LiveRamp ingestion price  
• Hive override history  
• LIFE platform price  

Includes discrepancy detection and classification.
""",
)
def get_segment_pricing_reconciliation(segment_id: str):
    return pricing_service.get_full_pricing_audit(segment_id)

@v1.post(
    "/pricing/reconciliation/bulk",
    tags=["Pricing"],
    summary="Bulk Pricing Reconciliation",
)
def bulk_reconciliation(payload: BulkReconciliationRequest):

    org_id = resolve_org_id(None)

    audits = [
        pricing_service.get_full_pricing_audit(segment_id, org_id)
        for segment_id in payload.segment_ids
    ]

    return {
        "total_checked": len(payload.segment_ids),
        "segments": audits,
    }


@v1.post(
    "/pricing/reconciliation/bulk/export",
    tags=["Pricing"],
    summary="Export Bulk Reconciliation to CSV",
)
def export_bulk_reconciliation(payload: BulkReconciliationRequest):

    org_id = resolve_org_id(None)

    audits = []

    for segment_id in payload.segment_ids:
        audit = pricing_service.get_full_pricing_audit(segment_id, org_id)
        audits.append(audit)

    output = StringIO()
    writer = csv.writer(output)

    # -----------------------------
    # Report Header
    # -----------------------------
    writer.writerow(["PulsePoint Pricing Reconciliation Report"])
    writer.writerow([f"Generated At (UTC): {datetime.utcnow().isoformat()}"])
    writer.writerow([])

    writer.writerow([
        "Segment ID",
        "LiveRamp Original Price ($)",
        "PulsePoint Override Price ($)",
        "LIFE Platform Price ($)",
        "Reconciliation Status",
        "Discrepancy Type",
        "Percent Difference",
        "Data Provider ID",
        "Data Provider Name",
        "Segment Size",
        "Segment Type",
        "Onboarder ID",
        "Onboarder Name",
    ])


    # -----------------------------
    # Write Rows
    # -----------------------------
    for audit in audits:

        current_prices = audit.get("current_prices", {})

        liveramp_price = current_prices.get("liveramp")
        override_price = current_prices.get("hive")
        life_price = current_prices.get("life")
   
        discrepancy = audit.get("discrepancy", False)
        discrepancy_type = audit.get("discrepancy_type", "")

        status = "Mismatch" if discrepancy else "Match"
        if status == "Match":
            discrepancy_type = "No Discrepancy"

        # -----------------------------
        # Variance Calculation
        # -----------------------------
        if life_price is None or override_price is None:
            variance_display = "N/A"
        else:
            variance = round(life_price - override_price, 2)
            if variance == 0:
                variance_display = "$0.00"
            elif variance > 0:
                variance_display = f"+${variance:.2f}"
            else:
                variance_display = f"-${abs(variance):.2f}"

        
        # -----------------------------
        # Percent Difference
        # -----------------------------
        if life_price is None or override_price is None or override_price == 0:
            percent_difference = None
        else:
            percent_difference = round(
               ((life_price - override_price) / override_price) * 100,
               2
            )

        # -----------------------------
        # Segment Metadata
        # -----------------------------
        segment_metadata = audit.get("segment_metadata", {})

        provider_id = segment_metadata.get("dataproviderid")
        onboarder_id = segment_metadata.get("onboarderid")
        segment_size = segment_metadata.get("segmentsize")

        provider_name = (
            pricing_service.get_provider_name(provider_id)
            if provider_id else None
        )
        onboarder_name = (
            pricing_service.get_account_name(onboarder_id)
            if onboarder_id else None
        )

        # -----------------------------
        # CSV Row
        # -----------------------------
        writer.writerow([
            audit.get("segment_id"),

            f"${liveramp_price:.2f}" if liveramp_price is not None else "N/A",
            f"${override_price:.2f}" if override_price is not None else "N/A",
            f"${life_price:.2f}" if life_price is not None else "N/A",

            status,
            discrepancy_type,

            # 👇 THIS IS WHERE IT GOES
            f"{percent_difference:.2f}%" if percent_difference is not None else "N/A",

            provider_id,
            provider_name if provider_name else f"Unmapped ({provider_id})",

            f"{segment_size:,}" if segment_size is not None else "",

            "1st Party" if segment_metadata.get("liverampcustom")
            else "Marketplace" if segment_metadata.get("liverampcustom") is not None
            else "Unknown",

            onboarder_id,
            onboarder_name if onboarder_name else f"Unknown ({onboarder_id})",
        ])


    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=pricing_reconciliation_report.csv"
        },
    )



@v1.get(
    "/pricing/reconciliation/search",
    tags=["Pricing"],
    summary="Segment Pricing Reconciliation — LiveRamp vs LIFE",
    description="""
Cross-system pricing reconciliation between LiveRamp taxonomy and the LIFE DSP platform.

Supports filtering by:
- `segment_id` — one or more LiveRamp segment IDs
- `provider_name` — partial match (e.g. "veeva", "crossix", "acxiom")
- `segment_type` — `firstparty` or `thirdparty`
- `sync_status` — `IN SYNC`, `PRICE MISMATCH`, `LR DELTA DETECTED`, `NOT IN LIFE`

Returns pricing from both systems with a `price_diff` and `sync_status` flag per segment.
""",
)
def search_segment_pricing_reconciliation(
    segment_id: Optional[List[str]] = Query(
        None,
        description="One or more LiveRamp segment IDs",
        example=["1001779766", "1011960131"],
    ),
    provider_name: Optional[str] = Query(
        None,
        description="Partial match on provider name (case-insensitive)",
        example="veeva",
    ),
    segment_type: Optional[str] = Query(
        None,
        description="Filter by segment source type",
        enum=["firstparty", "thirdparty"],
        example="thirdparty",
    ),
    sync_status: Optional[str] = Query(
        None,
        description="Filter by sync status",
        enum=["IN SYNC", "PRICE MISMATCH", "LR DELTA DETECTED", "NOT IN LIFE"],
        example="NOT IN LIFE",
    ),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=500, description="Results per page"),
):
    # --------------------------------------------------
    # Build WHERE clause dynamically
    # --------------------------------------------------
    filters = []

    if segment_id:
        ids_list = ", ".join(f"'{s}'" for s in segment_id)
        filters.append(f"segment_id IN ({ids_list})")

    if provider_name:
        filters.append(f"LOWER(provider_name) LIKE '%{provider_name.lower()}%'")

    if segment_type:
        filters.append(f"segment_type = '{segment_type}'")

    if sync_status:
        filters.append(f"sync_status = '{sync_status}'")

    where_clause = ("WHERE " + " AND ".join(filters)) if filters else ""

    offset = (page - 1) * page_size

    query = f"""
        WITH

        lr_latest_price AS (
            SELECT
                segment_id,
                provider_name,
                segment_name,
                price          AS lr_price,
                delta,
                day            AS lr_last_updated
            FROM (
                SELECT
                    *,
                    ROW_NUMBER() OVER (PARTITION BY segment_id ORDER BY day DESC) AS rn
                FROM iceberg.liveramp.taxonomy_historical
                WHERE price IS NOT NULL
            ) t
            WHERE rn = 1
        ),

        seg_source AS (
            SELECT
                segment_id,
                source,
                provider_id
            FROM (
                SELECT
                    *,
                    ROW_NUMBER() OVER (PARTITION BY segment_id ORDER BY day DESC) AS rn
                FROM iceberg.liveramp.segments_source
            ) s
            WHERE rn = 1
        ),

        advpixel_lr AS (
            SELECT
                REGEXP_EXTRACT(token, '[0-9]+')  AS segment_id,
                token,
                price           AS life_price,
                grossprice      AS life_grossprice,
                dataproviderid,
                ishealth,
                lastmodifieddate,
                accountid
            FROM portal.dbo.advpixel
            WHERE liverampcustom = true
              AND isactive = true
        ),

        reconciled AS (
            SELECT
                lr.segment_id,
                lr.provider_name,
                lr.segment_name,
                ss.source                               AS segment_type,
                a.token                                 AS life_token,
                a.life_price                            AS price_in_life,
                a.life_grossprice                       AS grossprice_in_life,
                lr.lr_price                             AS price_in_liveramp,
                CAST(lr.lr_price AS DOUBLE)
                    - CAST(a.life_price AS DOUBLE)      AS price_diff,
                lr.delta                                AS liveramp_delta,
                lr.lr_last_updated                      AS liveramp_price_last_updated,
                a.lastmodifieddate                      AS life_last_modified,
                CASE
                    WHEN a.segment_id IS NULL                                             THEN 'NOT IN LIFE'
                    WHEN CAST(a.life_price AS DOUBLE) != CAST(lr.lr_price AS DOUBLE)     THEN 'PRICE MISMATCH'
                    WHEN lr.delta IS NOT NULL                                             THEN 'LR DELTA DETECTED'
                    ELSE 'IN SYNC'
                END                                     AS sync_status
            FROM lr_latest_price lr
            LEFT JOIN seg_source ss  ON lr.segment_id = ss.segment_id
            LEFT JOIN advpixel_lr a  ON lr.segment_id = a.segment_id
        )

        SELECT *
        FROM reconciled
        {where_clause}
        ORDER BY sync_status DESC, provider_name, segment_id
        OFFSET {offset} ROWS
        FETCH FIRST {page_size} ROWS ONLY
    """

    print("\n==============================")
    print("EXECUTING SQL:")
    print(query)
    print("==============================\n")

    cursor = pricing_service.conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cols = [desc[0] for desc in cursor.description]

    results = [dict(zip(cols, row)) for row in rows]

    return {
        "page": page,
        "page_size": page_size,
        "count": len(results),
        "data": results,
    }



@v1.get(
    "/pricing/providers/summary",
    tags=["Pricing"],
    summary="Provider Pricing Summary — Live Snapshot of Active LiveRamp Custom Segments",
    description=(
        "Returns a real-time pricing summary grouped by data provider for all currently active LiveRamp custom segments stored in LIFE (portal.dbo.advpixel). "
        "Each result reflects the latest known state at the time the endpoint is called — no historical range is applied.\n\n"
        "Segments are classified as UNPRICED when their price_in_life value is zero, and PRICED when a non-zero price exists. "
        "Pricing source indicates whether the price originates from the LiveRamp Taxonomy (iceberg.liveramp.taxonomy_historical) or a direct contract arrangement (CONTRACT / DIRECT).\n\n"
        "Use this endpoint to audit provider-level pricing coverage, identify unpriced segment pools by provider, and support contract review or pricing reconciliation workflows. "
        "Supports filtering by provider name (partial match) and pricing status. "
        "Set include_segments=true to retrieve full segment-level detail alongside the summary."
    ),
)

def get_provider_pricing_summary(
    provider_name: Optional[str] = Query(
        None,
        description="Filter by provider name (partial match)",
        example="crossix",
    ),
    pricing_status: Optional[PricingStatus] = Query(
        None,
        description="Filter by pricing status",
        enum=["UNPRICED", "PRICED"],
        example="UNPRICED",
    ),
    include_segments: bool = Query(
        True,
        description="If true, includes segment-level detail in response",
    ),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=500),
):
    offset = (page - 1) * page_size

    provider_filter = f"AND LOWER(p.providername) LIKE '%{provider_name.lower()}%'" if provider_name else ""
    summary_status_filter = f"AND pricing_status = '{pricing_status.value}'" if pricing_status else ""

    # ADD THIS LINE

    query = f"""
        WITH lr_latest AS (
            SELECT segment_id, segment_name, CAST(price AS DOUBLE) AS lr_price
            FROM (
                SELECT segment_id, segment_name, price,
                    ROW_NUMBER() OVER (PARTITION BY segment_id ORDER BY day DESC) AS rn
                FROM iceberg.liveramp.taxonomy_historical
                WHERE price IS NOT NULL
            ) AS t
            WHERE rn = 1
        ),
        advpixel_segments AS (
            SELECT a.token, REGEXP_EXTRACT(a.token, '[0-9]+') AS segment_id, a.dataproviderid, p.providername, CAST(a.price AS DOUBLE) AS price_in_life, CAST(a.grossprice AS DOUBLE) AS grossprice_in_life, a.ishealth, a.lastmodifieddate, a.segmentsize
            FROM portal.dbo.advpixel a
            JOIN portal.dbo.segmentdataprovider p ON a.dataproviderid = p.id
            WHERE a.liverampcustom = true AND a.isactive = true
            {provider_filter}
        ),
        segment_detail AS (
            SELECT a.token, a.segment_id, a.dataproviderid, a.providername, a.price_in_life, a.grossprice_in_life, a.ishealth, a.lastmodifieddate, a.segmentsize, lr.segment_name,
            CASE WHEN lr.lr_price IS NOT NULL THEN 'LIVERAMP TAXONOMY' ELSE 'CONTRACT / DIRECT' END AS pricing_source,
            CASE WHEN a.price_in_life = 0 THEN 'UNPRICED' ELSE 'PRICED' END AS pricing_status
            FROM advpixel_segments a LEFT JOIN lr_latest lr ON a.segment_id = lr.segment_id
        ),
        segment_detail_filtered AS (
            SELECT * FROM segment_detail
            WHERE 1=1 {summary_status_filter}
        ),
        provider_summary AS (
            SELECT dataproviderid, providername,
                COUNT(*) AS total_segments,
                SUM(CASE WHEN pricing_status = 'UNPRICED' THEN 1 ELSE 0 END) AS unpriced_count,
                SUM(CASE WHEN pricing_status = 'PRICED' THEN 1 ELSE 0 END) AS priced_count,
                ROUND(AVG(price_in_life), 4) AS avg_price_in_life,
                ROUND(MIN(price_in_life), 4) AS min_price_in_life,
                ROUND(MAX(price_in_life), 4) AS max_price_in_life,
                MAX(pricing_source) AS pricing_source
            FROM segment_detail_filtered
            GROUP BY dataproviderid, providername
        )
        SELECT * FROM provider_summary
        ORDER BY unpriced_count DESC
        OFFSET {offset} ROWS
        FETCH FIRST {page_size} ROWS ONLY
    """

    print("\n==============================")
    print("EXECUTING SQL:")
    print(query)
    print("==============================\n")

    cursor = pricing_service.conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cols = [desc[0] for desc in cursor.description]
    summary = [dict(zip(cols, row)) for row in rows]

    segments = []
    if include_segments:
        seg_query = f"""
            WITH lr_latest AS (
                SELECT segment_id, segment_name, CAST(price AS DOUBLE) AS lr_price
                FROM (
                    SELECT segment_id, segment_name, price,
                        ROW_NUMBER() OVER (PARTITION BY segment_id ORDER BY day DESC) AS rn
                    FROM iceberg.liveramp.taxonomy_historical
                    WHERE price IS NOT NULL
                ) AS t
                WHERE rn = 1
            ),
            advpixel_segments AS (
                SELECT a.token, REGEXP_EXTRACT(a.token, '[0-9]+') AS segment_id, a.dataproviderid, p.providername, CAST(a.price AS DOUBLE) AS price_in_life, CAST(a.grossprice AS DOUBLE) AS grossprice_in_life, a.ishealth, a.lastmodifieddate, a.segmentsize
                FROM portal.dbo.advpixel a
                JOIN portal.dbo.segmentdataprovider p ON a.dataproviderid = p.id
                WHERE a.liverampcustom = true AND a.isactive = true
                {provider_filter}
            ),
            segment_detail AS (
                SELECT a.token, a.segment_id, a.dataproviderid, a.providername, a.price_in_life, a.grossprice_in_life, a.ishealth, a.lastmodifieddate, a.segmentsize, lr.segment_name,
                CASE WHEN lr.lr_price IS NOT NULL THEN 'LIVERAMP TAXONOMY' ELSE 'CONTRACT / DIRECT' END AS pricing_source,
                CASE WHEN a.price_in_life = 0 THEN 'UNPRICED' ELSE 'PRICED' END AS pricing_status
                FROM advpixel_segments a LEFT JOIN lr_latest lr ON a.segment_id = lr.segment_id
            ),
            segment_detail_filtered AS (
                SELECT * FROM segment_detail
                WHERE 1=1 {summary_status_filter}
            )
            SELECT * FROM segment_detail_filtered
            ORDER BY providername, price_in_life DESC
            OFFSET {offset} ROWS
            FETCH FIRST {page_size} ROWS ONLY
        """

        seg_cursor = pricing_service.conn.cursor()
        seg_cursor.execute(seg_query)
        seg_rows = seg_cursor.fetchall()
        seg_cols = [desc[0] for desc in seg_cursor.description]
        segments = [dict(zip(seg_cols, row)) for row in seg_rows]

    return {
        "page": page,
        "page_size": page_size,
        "count": len(summary),
        "provider_summary": summary,
        "segments": segments if include_segments else [],
    }


@v1.get(
    "/liveramp/destinations",
    response_model=DestinationListResponse,
    operation_id="list_destinations",
    tags=["Destination & Delivery"],
    summary="Destination Retrieval",
    description="Returns a list of available LiveRamp activation destinations.",
)
def list_destinations(
    limit: int = 10,
    after: Optional[str] = None,
):
    org_id = resolve_org_id(None)

    qp: List[Tuple[str, Union[str, int]]] = [("limit", limit)]
    if after:
        qp.append(("after", after))

    upstream = lr_request(
        "GET",
        "/activation/v2/destinations",
        org_id,
        query_params=qp,
    )

    return map_destinations_response(upstream)


@v1.get(
    "/liveramp/segments",
    response_model=SegmentListResponse,
    operation_id="list_first_party_segments",
    tags=["1st Party Data"],
    summary="Fetch First Party Segments",
)

def list_first_party_segments(
    limit: int = Query(50, ge=10, le=2000),
    after: Optional[str] = None,
    x_lr_org_id: Optional[str] = Header(None),
):
    org_id = resolve_org_id(x_lr_org_id)

    qp = [("limit", limit)]
    if after:
        qp.append(("after", after))

    upstream = lr_request(
        "GET",
        "/activation/v2/segments",
        org_id,
        query_params=qp,
    )

    return map_segments_response(upstream)



@v1.get(
    "/liveramp/marketplace/segments",
    response_model=MarketplaceSegmentListResponse,
    operation_id="list_marketplace_segments",
    tags=["3rd Party Marketplace"],
    summary="Full List of Marketplace Segments",
)

def list_marketplace_segments(
    limit: int = Query(
        5,
        ge=1,
        le=100,
        description="Number of marketplace segments to return",
    ),
    after: Optional[str] = Query(        # ← ADD THIS
        None,
        description="Pagination cursor from previous response to fetch next page",
    ),
    countryCodes: Optional[List[CountryCode]] = Query(
        default=["USA"],
        description="Country filter (ISO alpha-3)",
    ),
    currencyCodes: Optional[List[CurrencyCode]] = Query(
        default=["USD"],
        description="Currency filter",
    ),
    identifierType: Optional[List[IdentifierType]] = Query(
        default=["COOKIE"],
        description="Identifier type used for activation",
    ),
    x_lr_org_id: Optional[str] = Header(default=None, alias="X-LR-Org-Id"),
):
    org_id = resolve_org_id(x_lr_org_id)

    qp: List[Tuple[str, Union[str, int]]] = [("limit", limit)]
 
    if after:
        qp.append(("after", after))

    for c in countryCodes or []:
        qp.append(("countryCodes[]", c))

    for c in currencyCodes or []:
        qp.append(("currencyCodes[]", c))

    for it in identifierType or []:
        qp.append(("identifierType[]", it))

    upstream = lr_request(
        "GET",
        "/data-marketplace/buyer-api/v3/segments",
        org_id,
        query_params=qp,
    )

    return map_marketplace_segments_response(upstream)

@v1.get(
    "/liveramp/marketplace/segments/detail",
    response_model=MarketplaceSegmentDetailResponse,
    operation_id="get_marketplace_segment_detail",
    tags=["3rd Party Marketplace"],
    summary="Marketplace Segment Detail",
    description="Returns detailed metadata and pricing information for specific marketplace segment IDs.",
)

def marketplace_segments_detail(
    ids: Annotated[
        List[int],
        Query(
            ...,
            min_length=1,
            description="One or more LiveRamp Marketplace segment IDs. "
                        "Click 'Add integer item' and provide at least one ID. "
                        "Multiple IDs may be supplied.",
            example=[1012603801, 1012603871],
        ),
    ],
    limit: int = Query(10, ge=1, le=100),
    x_lr_org_id: Optional[str] = Header(default=None, alias="X-LR-Org-Id"),
):
    org_id = resolve_org_id(x_lr_org_id)

    qp: List[Tuple[str, Union[str, int]]] = [("limit", limit)]
    for seg_id in ids:
        qp.append(("ids", seg_id))

    upstream = lr_request(
        "GET",
        "/data-marketplace/buyer-api/v3/segments",
        org_id,
        query_params=qp,
    )

    return map_marketplace_segment_detail_response(upstream)


@v1.post(
    "/liveramp/requested-segments",
    response_model=RequestedSegmentsResponse,
    operation_id="request_marketplace_segments",
    tags=["3rd Party Marketplace"],
    summary="Activate Marketplace Segments",
    description="""
Activates third-party (Marketplace) segments for delivery to selected destinations.

This endpoint wraps the LiveRamp Marketplace activation workflow
and standardizes request and response formatting for PulsePoint internal usage.

Use this endpoint to:
- Enable Marketplace segments for activation
- Initiate third-party distribution workflows
- Activate purchased audience data

Returns activation results per segment.
""",
)
def request_segments_for_activation(
    payload: RequestedSegmentsRequest = Body(...),
):
    org_id = resolve_org_id(None)

    upstream_payload = map_requested_segments_request(payload)

    upstream = lr_request(
        "POST",
        "/data-marketplace/buyer-api/v3/requested-segments",
        org_id,
        json_body=upstream_payload,
    )

    return map_requested_segments_response(upstream)


@v1.get(
    "/liveramp/segment-statuses",
    response_model=SegmentStatusListResponse,
    operation_id="list_segment_statuses",
    tags=["Activation Monitoring"],
    summary="Fetch Activation Status (Marketplace & First-Party)",
    description="""
Retrieves activation statuses for LiveRamp segments.

Supports:
- DATA_MARKETPLACE (3rd party marketplace segments)
- ONBOARDING (1st party advertiser segments)

Returns activation state per destination.
""",
    responses={
        200: {
            "description": "Segment activation states across destinations",
            "content": {
                "application/json": {
                    "example": {
                        "statuses": [
                            {
                                "segment_id": 1015271391,
                                "destination_id": "cf46086e-df54-47f5-83b8-8115642c75c4",
                                "activation_state": "ACTIVE",
                                "last_updated": "2024-02-01T00:00:00Z"
                            }
                        ],
                        "pagination": {
                            "after": None,
                            "total": 6
                        }
                    }
                }
            }
        }
    },
)
def list_segment_statuses(
    segment_ids: List[int] = Query(
        ...,
        alias="segmentIDs[]",
        description="One or more LiveRamp segment IDs",
    ),
    segment_type: SegmentType = Query(
        ...,
        alias="segmentType",
        description="Segment type: DATA_MARKETPLACE or ONBOARDING",
    ),
    limit: int = Query(
        50,
        ge=1,
        le=2000,
        description="Max number of records to return",
    ),
):
    # ✅ Fully automated org resolution
    org_id = resolve_org_id(None)

    qp: List[Tuple[str, Union[str, int]]] = [("limit", limit)]

    for sid in segment_ids:
        qp.append(("segmentIDs[]", sid))

    qp.append(("segmentType", segment_type))

    upstream = lr_request(
        "GET",
        "/activation/v2/segment-statuses",
        org_id,
        query_params=qp,
    )

    return map_segment_statuses_response(upstream)

    return map_segment_statuses_response(upstream)


@v1.get(
    "/segment-updates",
    response_model=SegmentUpdatesResponse,
    tags=["Segment Updates"],
    summary="Retrieve marketplace segment update events",
)
def get_segment_updates(
    since: datetime = Query(
    ...,
    description="ISO 8601 timestamp (UTC). Example: 2026-03-01T00:00:00Z",
    example="2026-03-01T00:00:00Z",
),
    segment_id: Optional[int] = Query(
        None,
        description="Filter results to a specific segment ID",
    ),
    cursor: Optional[str] = Query(
        None,
        description="Pagination cursor",
    ),
):
    qp = {"since": since.isoformat()}
    if cursor:
        qp["cursor"] = cursor


    org_id = settings.LIVERAMP_ORG_ID  # or wherever you store it

    upstream = lr_request(
        "GET",
        "/data-marketplace/buyer-api/v3/segment-updates",
        org_id,
        query_params=qp,
    )

    updates = upstream.get("v3_SegmentUpdates", [])

    # 🔎 Filter by segment_id if provided
    if segment_id:
        updates = [
            u for u in updates
            if u.get("segmentId") == segment_id
        ]

    upstream["v3_SegmentUpdates"] = updates

    if not updates:
        return {
            "message": "No segment updates found for the given criteria.",
            "v3_SegmentUpdates": [],
            "nextCursor": upstream.get("nextCursor"),
        }

    return {
        "v3_SegmentUpdates": updates,
        "nextCursor": upstream.get("nextCursor"),
    }







@v1.get(
    "/liveramp/deliveries",
    response_model=DeliveryListResponse,
    operation_id="list_deliveries",
    tags=["Destination & Delivery"],
    summary="Segment Deliveries Per Connection",
)
def deliveries(
    integrationConnectionID: int = Query(
        ...,
        description="LiveRamp integration connection ID",
    ),
    limit: int = Query(
        50,
        ge=1,
        le=2000,
        description="Max number of records to return",
    ),
):
    # ✅ Fully automated org resolution
    org_id = resolve_org_id(None)

    qp: List[Tuple[str, Union[str, int]]] = [
        ("integrationConnectionID", integrationConnectionID),
        ("limit", limit),
    ]

    upstream = lr_request(
        "GET",
        "/activation/v2/deliveries",
        org_id,
        query_params=qp,
    )

    return map_deliveries_response(upstream)


@v1.get(
    "/pricing/price-changes/legacy",
    response_model=PriceChangeResponse,
    tags=["Pricing"],
    summary="Find LiveRamp price change events (Legacy Table)",
)
def get_price_changes_legacy(
    segment_id: Optional[int] = Query(
        None,
        description="Filter by specific segment ID",
        example=1000848846,
    ),
    start_date: Optional[date] = Query(
        None,
        description="Start date filter (YYYY-MM-DD)",
        example="2025-01-01",
    ),
    end_date: Optional[date] = Query(
        None,
        description="End date filter (YYYY-MM-DD)",
        example="2025-12-31",
    ),
    limit: int = Query(
        100,
        description="Maximum number of results to return",
        ge=1,
        le=1000,
        example=100,
    ),
):

    table = "gridhive.thirdparty.liveramp_taxonomy_historical"

    filters = []

    if segment_id is not None:
        filters.append(f"segment_id = '{segment_id}'")
    if start_date:
        filters.append(f"CAST(day AS DATE) >= DATE '{start_date}'")
    if end_date:
        filters.append(f"CAST(day AS DATE) <= DATE '{end_date}'")
    where_clause = ""
    if filters:
        where_clause = "WHERE " + " AND ".join(filters)

    query = f"""
        SELECT
            segment_id,
            segment_name,
            day,
            price AS new_price,
            prev_price AS old_price
        FROM (
            SELECT
                segment_id,
                segment_name,
                day,
                price,
                LAG(price) OVER (PARTITION BY segment_id ORDER BY day) AS prev_price
            FROM {table}
            {where_clause}
        ) t
        WHERE price <> prev_price
        ORDER BY segment_id, day
        LIMIT {limit}
    """

    cursor = pricing_service.conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    results = [
        {
            "segment_id": r[0],
            "segment_name": r[1],
            "day": r[2],
            "new_price": float(r[3]),
            "old_price": float(r[4]),
        }
        for r in rows
    ]

    return {
        "source": "legacy",
        "count": len(results),
        "results": results,
    }



@v1.get(
    "/pricing/price-changes/iceberg",
    response_model=PriceChangeResponse,
    tags=["Pricing"],
    summary="Find LiveRamp price change events (Iceberg Table)",
)
def get_price_changes_iceberg(
    segment_id: Optional[int] = Query(
        None,
        description="Filter by specific segment ID",
        example=1000848846,
    ),
    start_date: Optional[date] = Query(
        None,
        description="Start date filter (YYYY-MM-DD)",
        example="2026-01-01",
    ),
    end_date: Optional[date] = Query(
        None,
        description="End date filter (YYYY-MM-DD)",
        example="2026-03-01",
    ),
    limit: int = Query(
        100,
        description="Maximum number of results to return",
        ge=1,
        le=1000,
        example=100,
    ),
):

    table = "iceberg.liveramp.taxonomy_historical"

    filters = []

    # segment_id is VARCHAR in most LR tables
    if segment_id is not None:
        filters.append(f"segment_id = '{segment_id}'")

    # Iceberg usually stores day as DATE
    if start_date:
        filters.append(f"day >= '{start_date}'")
    if end_date:
        filters.append(f"day <= '{end_date}'")

    where_clause = ""
    if filters:
        where_clause = "WHERE " + " AND ".join(filters)

    query = f"""
        SELECT
            segment_id,
            segment_name,
            day,
            price AS new_price,
            prev_price AS old_price
        FROM (
            SELECT
                segment_id,
                segment_name,
                day,
                price,
                LAG(price) OVER (PARTITION BY segment_id ORDER BY day) AS prev_price
            FROM {table}
            {where_clause}
        ) t
        WHERE price <> prev_price
        ORDER BY segment_id, day
        LIMIT {limit}
    """

    
    print("\n==============================")
    print("EXECUTING SQL:")
    print(query)
    print("==============================\n")


    cursor = pricing_service.conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    results = [
        {
            "segment_id": r[0],
            "segment_name": r[1],
            "day": r[2],
            "new_price": float(r[3]),
            "old_price": float(r[4]),
        }
        for r in rows
    ]

    return {
        "source": "iceberg",
        "count": len(results),
        "results": results,
    }









@v1.post(
    "/liveramp/segments/distribute",
    response_model=FirstPartyDistributionResponse,
    operation_id="distribute_first_party_segments",
    tags=["1st Party Data"],
    summary="Activate First-Party Segments",
    description="""
Distributes first-party segments to configured LiveRamp destinations.

This endpoint wraps the LiveRamp Distribution API and
standardizes request and response formatting for PulsePoint internal usage.

Use this endpoint to:
- Distribute first-party owned segments
- Trigger activation workflows for internal data
- Initiate segment distribution to selected destinations

Returns distribution results per segment.
""",
)
def distribute_first_party_segments(
    request: FirstPartyDistributionRequest,
):
    org_id = resolve_org_id(None)

    grouped = defaultdict(list)
    for seg in request.segments:
        grouped[seg.destination_id].append(seg)

    all_results = []
    for destination_id, segments in grouped.items():
        sub_request = FirstPartyDistributionRequest(segments=segments)
        upstream_payload = map_first_party_distribution_request(sub_request)

        upstream = lr_request(
            "POST",
            f"/activation/v2/distribution-managers/{destination_id}/segment-configs",
            org_id,
            json_body=upstream_payload,
        )

        result = map_first_party_distribution_response(upstream, sub_request)
        all_results.extend(result.results)

    return FirstPartyDistributionResponse(results=all_results)


app.include_router(v1)


# ----------------------------
# Legacy (non-versioned) routes (deprecated) - keep protected
# ----------------------------
legacy = APIRouter(
    prefix="",
    dependencies=[Depends(require_pp_api_key_security)],
    tags=["legacy"],
)


@legacy.get("/health", deprecated=True)
def health_legacy():
    return health()


@legacy.get("/liveramp/destinations", deprecated=True)
def destinations_legacy(
    limit: int = Query(1, ge=1, le=200),
    after: Optional[str] = Query(default=None),
    x_lr_org_id: Optional[str] = Header(default=None, alias="X-LR-Org-Id"),
):
    return list_destinations(limit=limit, after=after, x_lr_org_id=x_lr_org_id)


@legacy.get("/liveramp/segments", deprecated=True)
def segments_legacy(
    limit: int = Query(50, ge=10, le=2000),
    after: Optional[str] = Query(default=None),
    x_lr_org_id: Optional[str] = Header(default=None, alias="X-LR-Org-Id"),
):
    return list_first_party_segments(limit=limit, after=after, x_lr_org_id=x_lr_org_id)


@legacy.get("/liveramp/marketplace/segments", deprecated=True)
def marketplace_segments_legacy(
    limit: int = Query(5, ge=1, le=100),
    countryCodes: Optional[List[str]] = Query(default=["USA"]),
    currencyCodes: Optional[List[str]] = Query(default=["USD"]),
    identifierType: Optional[List[str]] = Query(default=["COOKIE"]),
    x_lr_org_id: Optional[str] = Header(default=None, alias="X-LR-Org-Id"),
):
    return list_marketplace_segments(
        limit=limit,
        countryCodes=countryCodes,
        currencyCodes=currencyCodes,
        identifierType=identifierType,
        x_lr_org_id=x_lr_org_id,
    )


@legacy.get("/liveramp/marketplace/segments/detail", deprecated=True)
def marketplace_detail_legacy(
    limit: int = Query(10, ge=1, le=100),
    ids: List[int] = Query(...),
    x_lr_org_id: Optional[str] = Header(default=None, alias="X-LR-Org-Id"),
):
    return marketplace_segments_detail(limit=limit, ids=ids, x_lr_org_id=x_lr_org_id)


@legacy.post("/liveramp/requested-segments", deprecated=True)
def requested_segments_legacy(
    payload: List[Dict[str, Any]] = Body(...),
    x_lr_org_id: Optional[str] = Header(default=None, alias="X-LR-Org-Id"),
):
    return request_segments_for_activation(payload=payload, x_lr_org_id=x_lr_org_id)


@legacy.get("/liveramp/segment-statuses", deprecated=True)
def segment_statuses_legacy(
    segmentIDs: List[int] = Query(...),
    segmentType: str = Query("DATA_MARKETPLACE"),
    limit: int = Query(1, ge=1, le=200),
    x_lr_org_id: Optional[str] = Header(default=None, alias="X-LR-Org-Id"),
):
    return segment_statuses(
        segmentIDs=segmentIDs,
        segmentType=segmentType,
        limit=limit,
        x_lr_org_id=x_lr_org_id,
    )


@legacy.get("/liveramp/deliveries", deprecated=True)
def deliveries_legacy(
    integrationConnectionID: str = Query(...),
    x_lr_org_id: Optional[str] = Header(default=None, alias="X-LR-Org-Id"),
):
    return deliveries(integrationConnectionID=integrationConnectionID, x_lr_org_id=x_lr_org_id)


app.include_router(legacy)


# ----------------------------
# OpenAPI 3.0.3 export override
# - FastAPI may emit 3.1.0 schemas depending on version.
# - OpenAPI Generator 7.6.0 has issues with 3.1.0.
# - This converts common "null" patterns into OpenAPI 3.0 "nullable".
# ----------------------------
def _to_openapi30_nullable(schema: Any) -> Any:
    """
    Convert common OpenAPI 3.1 / JSON Schema patterns into OpenAPI 3.0-compatible nullable.
    Handles:
      - {"type": ["string","null"]} -> {"type":"string","nullable": True}
      - {"anyOf": [X, {"type":"null"}]} -> X + nullable
      - {"oneOf": [X, {"type":"null"}]} -> X + nullable
    Applies recursively.
    """
    if isinstance(schema, list):
        return [_to_openapi30_nullable(x) for x in schema]

    if not isinstance(schema, dict):
        return schema

    # Recurse first
    for k, v in list(schema.items()):
        schema[k] = _to_openapi30_nullable(v)

    # type: ["T","null"] -> type: "T", nullable: true
    t = schema.get("type")
    if isinstance(t, list) and "null" in t:
        non_null = [x for x in t if x != "null"]
        if len(non_null) == 1:
            schema["type"] = non_null[0]
            schema["nullable"] = True
        else:
            schema["type"] = non_null
            schema["nullable"] = True

    # anyOf/oneOf with a null branch -> nullable
    for comb in ("anyOf", "oneOf"):
        if comb in schema and isinstance(schema[comb], list):
            variants = schema[comb]
            null_variants = [v for v in variants if isinstance(v, dict) and v.get("type") == "null"]
            if null_variants:
                non_null_variants = [v for v in variants if v not in null_variants]
                if len(non_null_variants) == 1 and isinstance(non_null_variants[0], dict):
                    merged = non_null_variants[0]
                    merged["nullable"] = True
                    for keep in ("title", "description", "default", "example", "examples"):
                        if keep in schema and keep not in merged:
                            merged[keep] = schema[keep]
                    schema.clear()
                    schema.update(merged)
                else:
                    schema[comb] = non_null_variants
                    schema["nullable"] = True

    return schema


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
        openapi_version="3.0.3",
    )

    # Remove OpenAPI 3.1-only fields if present
    schema.pop("jsonSchemaDialect", None)

    # Convert component schemas
    comps = schema.get("components", {})
    comp_schemas = comps.get("schemas", {})
    for name, sch in list(comp_schemas.items()):
        comp_schemas[name] = _to_openapi30_nullable(sch)

    # Convert inline schemas under paths
    paths = schema.get("paths", {})
    for _, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue
        for _, op in path_item.items():
            if not isinstance(op, dict):
                continue

            # parameters
            params = op.get("parameters", [])
            for p in params:
                if isinstance(p, dict) and "schema" in p:
                    p["schema"] = _to_openapi30_nullable(p["schema"])

            # requestBody
            rb = op.get("requestBody")
            if isinstance(rb, dict):
                content = rb.get("content", {})
                for _, media in content.items():
                    if isinstance(media, dict) and "schema" in media:
                        media["schema"] = _to_openapi30_nullable(media["schema"])

            # responses
            responses = op.get("responses", {})
            for _, resp in responses.items():
                if not isinstance(resp, dict):
                    continue
                content = resp.get("content", {})
                for _, media in content.items():
                    if isinstance(media, dict) and "schema" in media:
                        media["schema"] = _to_openapi30_nullable(media["schema"])

    app.openapi_schema = schema
    return app.openapi_schema


app.openapi = custom_openapi
