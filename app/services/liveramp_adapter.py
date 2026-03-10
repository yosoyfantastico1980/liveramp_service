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
    Delivery,
    DeliveryListResponse,
    ActivationState,
    FirstPartyDistributionInput,    # ✅ ADD
    FirstPartyDistributionRequest,  # ✅ ADD
    FirstPartyDistributionResult,   # ✅ ADD
    FirstPartyDistributionResponse, # ✅ ADD
)

# ----------------------------
# Activation State Mapping
# ----------------------------

def map_liveramp_status_to_activation_state(lr_status: str) -> ActivationState:
    if not lr_status:
        return ActivationState.UNKNOWN

    status = lr_status.upper()

    # Taxonomy sync states
    if status in ["SYNCED"]:
        return ActivationState.ACTIVE

    if status in ["NOT_SYNCED"]:
        return ActivationState.PENDING

    # Generic states
    if status in ["REQUESTED", "PENDING", "PROCESSING"]:
        return ActivationState.PENDING

    if status in ["DELIVERING", "ACTIVE", "LIVE"]:
        return ActivationState.ACTIVE

    if status in ["FAILED", "ERROR", "REJECTED"]:
        return ActivationState.FAILED

    if status in ["PAUSED", "STOPPED"]:
        return ActivationState.PAUSED

    return ActivationState.UNKNOWN

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


    raw_total = raw_pagination.get("total")

    if isinstance(raw_total, int):
        normalized_total = raw_total
    elif isinstance(raw_total, str) and raw_total.isdigit():
        normalized_total = int(raw_total)
    else:
        normalized_total = None

    pagination = {
        "after": raw_pagination.get("after"),
        "total": normalized_total,
    }

 
    return DestinationListResponse(
        destinations=destinations,
        pagination=pagination,
    )


# ----------------------------
# Segments
# ----------------------------

def map_segments_response(upstream: dict) -> SegmentListResponse:
    raw_segments = upstream.get("v3_Segments", [])
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

    pagination = {
        "after": upstream.get("after"),
        "total": upstream.get("total"),
    }

    return SegmentListResponse(
        segments=segments,
        pagination=pagination,
    )

def map_marketplace_segments_response(upstream: dict) -> MarketplaceSegmentListResponse:
    """
    Transforms raw LiveRamp marketplace segments response into
    our stable v1 API contract.
    """

    raw_segments = upstream.get("v3_Segments", [])
    raw_pagination = upstream.get("_pagination", {})

    segments: List[MarketplaceSegment] = []

    for s in raw_segments:
        pricing = s.get("pricing", {})
        digital_price = pricing.get("digitalAdTargeting", {})

        segments.append(
            MarketplaceSegment(
                id=str(s.get("id")),
                name=s.get("name", ""),
                provider=s.get("providerName"),
                description=s.get("description"),
                segmentType=s.get("segmentType"),
                providerComments=s.get("providerComments"),
                identifierType=s.get("identifierType"),
                updatedAt=s.get("updatedAt"),
                countryCode=s.get("dataSourceLocation", {}).get("code"),
                location=s.get("dataSourceLocation", {}).get("location"),
                digitalAdTargetingPriceUSD=digital_price.get("value", {}).get("amount"),
            )
        )

    return MarketplaceSegmentListResponse(
        segments=segments,
        pagination={
            "after": raw_pagination.get("after"),
            "total": len(segments),
        },
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
        segment_id = r.get("id")          # was "segmentId"
        request_id = r.get("requestId")

        raw_status = r.get("status")

        if isinstance(raw_status, dict):
            status = raw_status.get("message", "UNKNOWN")  # just get the message
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



def map_first_party_distribution_request(request: FirstPartyDistributionRequest) -> list:
    return [
        {
            "segmentID": str(seg.segment_id),                          # was "segmentId", must be string
            "segmentType": "ONBOARDING",                               # required by LiveRamp for 1st party
            "distributionManagerID": str(seg.destination_id),         # was "destinationId", must be string
            **({"identifierType": seg.identifier_type.value} if seg.identifier_type else {})
        }
        for seg in request.segments
    ]


def map_first_party_distribution_response(upstream: Any, request: FirstPartyDistributionRequest) -> FirstPartyDistributionResponse:
    results = []
    for item in upstream:
        status_obj = item.get("status", {})
        # Match upstream result back to original request by segment_id
        original = next((s for s in request.segments if s.segment_id == item.get("id")), None)
        results.append(FirstPartyDistributionResult(
            segment_id=item.get("id"),
            destination_id=original.destination_id if original else None,
            status=status_obj.get("message", "UNKNOWN"),
            distribution_id=str(item.get("id")) if item.get("id") else None
        ))
    return FirstPartyDistributionResponse(results=results)



def map_segment_statuses_response(upstream: dict) -> SegmentStatusListResponse:
    raw_statuses = upstream.get("v2/SegmentStatuses", [])
    raw_pagination = upstream.get("_pagination", {})

    statuses = []

    for s in raw_statuses:
        statuses.append(
            SegmentStatus(
                segment_id=int(s.get("segmentID")) if s.get("segmentID") else None,
                destination_id=s.get("integrationConnectionID"),
                activation_state=map_liveramp_status_to_activation_state(
                    s.get("taxonomy", {}).get("taxonomySyncStatus")
                ),
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
            delivery_id=d.get("id"),
            segment_id=None,
            device_type=d.get("deviceType"),
            destination_id=d.get("integrationConnectionID"),
            status=d.get("status"),
            created_at=d.get("updatedAt"),
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

    # 👇 OUTSIDE THE LOOP (4 spaces only)
    total_count = len(segments)

    return MarketplaceSegmentDetailResponse(
        segments=segments,
        pagination={
            "after": raw_pagination.get("after"),
            "total": total_count,
        },
    )

