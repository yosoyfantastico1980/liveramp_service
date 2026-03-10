import os
from datetime import datetime
from typing import List, Dict, Optional

import trino
from trino.auth import BasicAuthentication


class PricingService:

    def __init__(self):

        self.conn = trino.dbapi.connect(
            host=os.getenv("TRINO_HOST"),
            port=int(os.getenv("TRINO_PORT", 8443)),
            user=os.getenv("TRINO_USER"),
            http_scheme="https",
            auth=BasicAuthentication(
                os.getenv("TRINO_USER"),
                os.getenv("TRINO_PASSWORD"),
            ),
            catalog="gridhive",
        )

    # =========================================================
    # Hive Historical Overrides
    # =========================================================
    def fetch_hive_history(self, segment_id: str, org_id: Optional[str] = None) -> List[Dict]:

        cursor = self.conn.cursor()

        # Basic sanitization (since Trino DBAPI does not always support params cleanly)
        safe_segment_id = segment_id.replace("'", "")

        query = f"""
            SELECT 
                 segment_id,
                 price, day
            FROM gridhive.thirdparty.liveramp_taxonomy_historical
            WHERE segment_id = '{safe_segment_id}'
            ORDER BY day
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        seen = set()
        records = []

        for seg_id, price, day in rows:
            key = (price, day)
            if key in seen:
                continue
            seen.add(key)

            records.append({
                "price": float(price),
                "effective_at": datetime.strptime(day, "%Y-%m-%d"),
                "source": "hive_override",
            })

        # Remove consecutive identical prices
        records = sorted(records, key=lambda r: r["effective_at"])

        deduped = []
        for record in records:
            if not deduped or deduped[-1]["price"] != record["price"]:
                deduped.append(record)

        return deduped


    # =========================================================
    # LIFE Platform Pricing
    # =========================================================
    def fetch_life_price(self, segment_id: str) -> List[Dict]:
        cursor = self.conn.cursor()
        safe_segment_id = segment_id.replace("'", "")

        query = f"""
            SELECT
                price,
                createdon,
                lastmodifieddate,
                dataproviderid,
                segmentsize,
                liverampcustom,
                onboarderid
            FROM portal.dbo.advpixel
            WHERE token LIKE '%{safe_segment_id}%'
            ORDER BY lastmodifieddate DESC
            LIMIT 1
        """

        cursor.execute(query)
        row = cursor.fetchone()

        if not row:
            return []

        (
            price,
            createdon,
            lastmodified,
            dataproviderid,
            segmentsize,
            liverampcustom,
            onboarderid,
        ) = row

        return [{
            "price": float(price),
            "effective_at": lastmodified or createdon,
            "source": "life_platform",
            "dataproviderid": dataproviderid,
            "segmentsize": segmentsize,
            "liverampcustom": liverampcustom,
            "onboarderid": onboarderid,
        }]


    # =========================================================
    # LiveRamp Base Price (Stub)
    # =========================================================
    def fetch_liveramp_base_price(self, segment_id: str) -> Dict:

        try:
            # Call your existing marketplace detail logic
            detail = self.fetch_liveramp_marketplace_detail(segment_id)

            if detail and detail.get("price") is not None:
                return detail

        except Exception as e:
            print(f"LiveRamp fetch failed: {e}")

        # Fallback (keeps system stable if anything breaks)
        return {
            "price": 4.00,
            "effective_at": datetime.utcnow(),
            "currency": "USD",
        }


    def fetch_liveramp_marketplace_detail(self, segment_id: str):

        try:
            from app.main import lr_request, resolve_org_id

            org_id = resolve_org_id(None)

            qp = [
                ("limit", 1),
                ("ids", int(segment_id)),
            ]

            upstream = lr_request(
                "GET",
                "/data-marketplace/buyer-api/v3/segments",
                org_id,
                query_params=qp,
            )

            print("UPSTREAM RAW:", upstream)

            if not upstream or "v3_Segments" not in upstream:
                return None

            segments = upstream.get("v3_Segments", [])
            if not segments:
                return None

            segment = segments[0]

            pricing = segment.get("pricing", {})
            digital = pricing.get("digitalAdTargeting")

            if not digital:
                return None

            amount = digital.get("value", {}).get("amount")
            currency = digital.get("currencyCode", "USD")

            if not amount:
                return None

            return {
                "price": amount / 100,
                "effective_at": datetime.utcnow(),
                "currency": currency,
            }

        except Exception as e:
            print(f"Marketplace pricing fetch failed: {e}")
            return None


    # =========================================================
    # Basic Pricing Endpoint (Existing)
    # =========================================================
    def get_pricing_history(self, segment_id: str, org_id: Optional[str] = None) -> Dict:

        base_price = self.fetch_liveramp_base_price(segment_id)
        hive_history = self.fetch_hive_history(segment_id, org_id)

        full_history = [
            {
                "price": base_price["price"],
                "effective_at": base_price["effective_at"],
                "source": "liveramp_ingestion",
            }
        ] + hive_history

        full_history = sorted(full_history, key=lambda r: r["effective_at"])
        current_price = full_history[-1]["price"]

        return {
            "segment_id": segment_id,
            "original_price": base_price["price"],
            "current_price": current_price,
            "currency": base_price.get("currency", "USD"),
            "pricing_history": full_history,
        }

    # =========================================================
    # FULL CROSS-SYSTEM RECONCILIATION
    # =========================================================
    def get_full_pricing_audit(self, segment_id: str, org_id: Optional[str] = None) -> Dict:

        base = self.fetch_liveramp_base_price(segment_id)
        hive = self.fetch_hive_history(segment_id, org_id)
        life = self.fetch_life_price(segment_id)

        life_metadata = life[-1] if life else {}

        timeline = [
            {
                "price": base["price"],
                "effective_at": base["effective_at"],
                "source": "liveramp_ingestion",
            }
        ] + hive + life

        timeline = sorted(timeline, key=lambda r: r["effective_at"])

        current_prices = {
            "liveramp": base["price"],
            "hive": hive[-1]["price"] if hive else base["price"],
            "life": life[-1]["price"] if life else None,
        }

        # Only compare real numeric values
        valid_prices = [
            p for p in current_prices.values()
            if p is not None
        ]

        discrepancy = len(set(valid_prices)) > 1

        # Optional: classify discrepancy severity
        discrepancy_type = None
        if discrepancy:
            if current_prices["life"] != current_prices["hive"]:
                discrepancy_type = "LIFE vs Override Mismatch"
            elif current_prices["hive"] != current_prices["liveramp"]:
                discrepancy_type = "PulsePoint Override"
            else:
                discrepancy_type = "General Price Variation"
 
        return {
            "segment_id": segment_id,
            "timeline": timeline,
            "current_prices": current_prices,
            "discrepancy": discrepancy,
            "discrepancy_type": discrepancy_type,

            "segment_metadata": {
                "dataproviderid": life_metadata.get("dataproviderid"),
                "segmentsize": life_metadata.get("segmentsize"),
                "liverampcustom": life_metadata.get("liverampcustom"),
                "onboarderid": life_metadata.get("onboarderid"),
            },
         }

    def get_account_name(self, account_id: int):
        if not account_id:
            return None

        # Known onboarder mapping
        if account_id == 41:
            return "LiveRamp"

        cursor = self.conn.cursor()

        query = f"""
            SELECT accountname
            FROM portal.dbo.account
            WHERE accountid = {account_id}
            LIMIT 1
        """

        cursor.execute(query)
        row = cursor.fetchone()

        if not row:
            return None

        return row[0]


    def get_provider_name(self, provider_id: int):
        if not provider_id:
            return None

        # Known static mappings
        if provider_id == 41:
            return "LiveRamp"

        cursor = self.conn.cursor()

        query = f"""
            SELECT name
            FROM portal.dbo.segmentsprovidernamemapping
            WHERE portal_id = {provider_id}
            LIMIT 1
        """

        cursor.execute(query)
        row = cursor.fetchone()

        if not row:
            return None

        return row[0]
