from typing import List, Dict, Any

from models.liveramp import (
    Destination,
    Pagination,
    DestinationListResponse,
    Segment,
    SegmentListResponse,
    MarketplaceSegmentDetail,
    MarketplaceSegmentDetailResponse,
    MarketplacePricing,   
    MarketplaceSegment,
    MarketplaceSegmentListResponse,
    RequestedSegmentInput,
    RequestedSegmentsRequest,
    RequestedSegmentResult,
    RequestedSegmentsResponse,
    SegmentStatus,
    SegmentStatusListResponse,
    Delivery,                 # ✅ ADD
    DeliveryListResponse,     # ✅ ADD
)

# ----------------------------
# Destinations
# ----------------------------

def map_destinations_response(upstream: dict) -> DestinationListResponse:
    raw_destinations = upstream.get("v2/Destinations", [])
    raw_pagination = upstream.get("_pagination", {})

    destinations = [
        Destination(
            id=str(d.get("id")),
            name=d.get("name") or "",
            logo_url=d.get("logoUrl"),
        )
        for d in raw_destinations
    ]

    pagination = Pagination(
        after=raw_pagination.get("after"),
        total=raw_pagination.get("total"),
    )

    return DestinationListResponse(
        destinations=destinations,
        pagination=pagination,
    )


# ----------------------------
# Segments
# ----------------------------

def map_segments_response(upstream: dict) -> SegmentListResponse:
    raw_segments = upstream.get("v2/Segments", [])
    raw_pagination = upstream.get("_pagination", {})

    segments = [
        Segment(
            id=str(s.get("id")),
            name=str(s.get("name") or ""),
            description=s.get("description"),
        )
        for s in raw_segments
    ]

    pagination = Pagination(
        after=raw_pagination.get("after"),
        total=raw_pagination.get("total"),
    )

    return SegmentListResponse(
        segments=segments,
        pagination=pagination,
    )

def map_marketplace_segments_response(upstream: dict) -> MarketplaceSegmentListResponse:
    """
    Transforms raw LiveRamp marketplace segments response into
    our stable v1 API contract.

    LiveRamp currently returns:
    {
      "v2/MarketplaceSegments": [...],
      "_pagination": {...}
    }
    """

    raw_segments = upstream.get("v2/MarketplaceSegments", [])
    raw_pagination = upstream.get("_pagination", {})

    segments = [
        MarketplaceSegment(
            id=str(s.get("id")),
            name=str(s.get("name") or ""),
            provider=s.get("provider"),
        )
        for s in raw_segments
    ]

    pagination = Pagination(
        after=raw_pagination.get("after"),
        total=raw_pagination.get("total"),
    )

    return MarketplaceSegmentListResponse(
        segments=segments,
        pagination=pagination,
    )

def map_requested_segments_request(
    request: RequestedSegmentsRequest,
) -> List[Dict[str, Any]]:
    """
    Converts our stable v1 request into
    LiveRamp upstream format.
    """

    return [
        {
            "segmentId": r.segment_id,
            "destinationId": r.destination_id,
            "identifierType": r.identifier_type,
        }
        for r in request.segments
    ]


def map_requested_segments_response(upstream: Any) -> RequestedSegmentsResponse:
    results = []

    for r in upstream or []:
        segment_id = r.get("segmentId")
        request_id = r.get("requestId")

        # LiveRamp sometimes returns status as an object
        raw_status = r.get("status")

        if isinstance(raw_status, dict):
            status = raw_status.get("error") or str(raw_status)
        else:
            status = raw_status

        results.append(
            RequestedSegmentResult(
                segment_id=int(segment_id) if segment_id else None,
                request_id=request_id,
                status=status,
            )
        )

    return RequestedSegmentsResponse(results=results)


def map_segment_statuses_response(upstream: dict) -> SegmentStatusListResponse:
    raw_statuses = upstream.get("v2/SegmentStatuses", [])
    raw_pagination = upstream.get("_pagination", {})

    statuses = []

    for s in raw_statuses:
        statuses.append(
            SegmentStatus(
                segment_id=int(s.get("segmentID")) if s.get("segmentID") else None,
                destination_id=int(s.get("destinationID")) if s.get("destinationID") else None,
                status=s.get("status"),
                last_updated=s.get("lastUpdated"),
            )
        )

    pagination = Pagination(
        after=raw_pagination.get("after"),
        total=raw_pagination.get("total"),
    )

    return SegmentStatusListResponse(
        statuses=statuses,
        pagination=pagination,
    )

def map_deliveries_response(upstream: dict) -> DeliveryListResponse:
    raw_deliveries = upstream.get("v2/Deliveries", [])
    raw_pagination = upstream.get("_pagination", {})

    deliveries = [
        Delivery(
            delivery_id=d.get("deliveryID"),
            segment_id=d.get("segmentID"),
            destination_id=d.get("integrationConnectionID"),
            status=d.get("status"),
            created_at=d.get("createdAt"),
        )
        for d in raw_deliveries
    ]

    pagination = Pagination(
        after=raw_pagination.get("after"),
        total=raw_pagination.get("total"),
    )

    return DeliveryListResponse(
        deliveries=deliveries,
        pagination=pagination,
    )

def map_marketplace_segment_detail_response(
    upstream: dict,
) -> MarketplaceSegmentDetailResponse:

    print("UPSTREAM DETAIL RESPONSE:", upstream)

    raw_segments = upstream.get("v3_Segments", [])
    raw_pagination = upstream.get("_pagination", {})

    segments = []

    for s in raw_segments:

        # Normalize pricing
        pricing_raw = s.get("pricing", {}) or {}
        pricing_list = []

        for use_case, value in pricing_raw.items():
            pricing_list.append(
                MarketplacePricing(
                    use_case=use_case,
                    currency_code=value.get("currencyCode"),
                    amount=value.get("value", {}).get("amount"),
                    unit=value.get("value", {}).get("unit"),
                )
            )

        segments.append(
            MarketplaceSegmentDetail(
                segment_id=int(s.get("id")) if s.get("id") else None,
                name=s.get("name"),
                description=s.get("description"),
                category=s.get("segmentType"),
                country_codes=(
                    [s.get("dataSourceLocation", {}).get("code")]
                    if s.get("dataSourceLocation", {}).get("code")
                    else None
                ),
                currency_codes=None,
                identifier_types=(
                    [s.get("identifierType")]
                    if isinstance(s.get("identifierType"), str)
                    else s.get("identifierType")
                ),
                pricing=pricing_list or None,
            )
        )

    return MarketplaceSegmentDetailResponse(
        segments=segments,
        pagination=Pagination(
            after=raw_pagination.get("after"),
            total=raw_pagination.get("total"),
        ),
    )
