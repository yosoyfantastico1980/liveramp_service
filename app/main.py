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

import certifi


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
    DeliveryListResponse,   # ✅ ADD HERE
    IdentifierType,
    CountryCode,
    CurrencyCode,
    SegmentType,
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
    map_deliveries_response,   # ✅ ADD HERE
)

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
    # NOTE: Some FastAPI versions still emit 3.1.0.
    # We override app.openapi below to force a 3.0.3-shaped schema for SDK generation.
    openapi_version="3.0.3",
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
v1 = APIRouter(prefix="/v1", tags=["v1"])


@v1.get("/health")
def health():
    return {"status": "ok"}


@v1.get("/ready")
def ready(
    x_lr_org_id: Optional[str] = Header(default=None, alias="X-LR-Org-Id"),
):
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
    "/liveramp/destinations",
    response_model=DestinationListResponse,
    operation_id="list_destinations",
)

def list_destinations(
    limit: int = 10,
    after: Optional[str] = None,
    x_lr_org_id: Optional[str] = Header(default=None, alias="X-LR-Org-Id"),
):
    org_id = resolve_org_id(x_lr_org_id)

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

    print("USING ADAPTER")  # ← ADD THIS LINE

    return map_segments_response(upstream)



@v1.get(
    "/liveramp/marketplace/segments",
    response_model=MarketplaceSegmentListResponse,
    operation_id="list_marketplace_segments",
)

def list_marketplace_segments(
    limit: int = Query(
        5,
        ge=1,
        le=100,
        description="Number of marketplace segments to return",
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
    operation_id="request_segments",
)

def request_segments_for_activation(
    payload: RequestedSegmentsRequest = Body(...),
    x_lr_org_id: Optional[str] = Header(default=None, alias="X-LR-Org-Id"),
):
    org_id = resolve_org_id(x_lr_org_id)

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
    operation_id="get_segment_statuses",
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
        description="Type of segment",
    ),
    limit: int = Query(
        50,
        ge=1,
        le=2000,
        description="Max number of records to return",
    ),
    x_lr_org_id: Optional[str] = Header(default=None, alias="X-LR-Org-Id"),
):

    org_id = resolve_org_id(x_lr_org_id)

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


@v1.get(
    "/liveramp/deliveries",
    response_model=DeliveryListResponse,
    operation_id="list_deliveries",
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
    x_lr_org_id: Optional[str] = Header(default=None, alias="X-LR-Org-Id"),
):
    org_id = resolve_org_id(x_lr_org_id)

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
