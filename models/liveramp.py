from enum import Enum
from pydantic import BaseModel
from typing import List, Optional


class Destination(BaseModel):
    """
    Stable representation of a LiveRamp destination
    exposed through our v1 API.
    """
    id: str
    name: str
    logo_url: Optional[str] = None


class Pagination(BaseModel):
    """
    Standardized pagination object returned by our API.
    """
    after: Optional[str] = None
    total: Optional[int] = None


class DestinationListResponse(BaseModel):
    """
    Response model for:
    GET /v1/liveramp/destinations
    """
    destinations: List[Destination]
    pagination: Pagination

class Segment(BaseModel):
    id: str
    name: str
    description: Optional[str] = None


class SegmentListResponse(BaseModel):
    segments: List[Segment]
    pagination: Pagination

class MarketplaceSegment(BaseModel):
    id: str
    name: str
    provider: Optional[str] = None


class MarketplaceSegmentListResponse(BaseModel):
    segments: List[MarketplaceSegment]
    pagination: Pagination

class RequestedSegmentInput(BaseModel):
    segment_id: int
    destination_id: int
    identifier_type: Optional[str] = None


class RequestedSegmentsRequest(BaseModel):
    segments: List[RequestedSegmentInput]

class RequestedSegmentResult(BaseModel):
    segment_id: Optional[int] = None
    request_id: Optional[str] = None
    status: Optional[str] = None


class RequestedSegmentsResponse(BaseModel):
    results: List[RequestedSegmentResult]

class SegmentStatus(BaseModel):
    segment_id: int
    destination_id: Optional[int] = None
    status: Optional[str] = None
    last_updated: Optional[str] = None


class SegmentStatusListResponse(BaseModel):
    statuses: List[SegmentStatus]
    pagination: Pagination

class SegmentType(str, Enum):
    DATA_MARKETPLACE = "DATA_MARKETPLACE"
    FIRST_PARTY = "FIRST_PARTY"

class IdentifierType(str, Enum):
    COOKIE = "COOKIE"
    MAID = "MAID"
    CTV = "CTV"
    EMAIL = "EMAIL"

class CountryCode(str, Enum):
    USA = "USA"

class CurrencyCode(str, Enum):
    USD = "USD"

class Delivery(BaseModel):
    delivery_id: Optional[str] = None
    segment_id: Optional[int] = None
    destination_id: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None


class DeliveryListResponse(BaseModel):
    deliveries: List[Delivery]
    pagination: Pagination

class MarketplacePricingValue(BaseModel):
    amount: Optional[int] = None
    unit: Optional[str] = None


class MarketplacePricing(BaseModel):
    use_case: str
    currency_code: Optional[str] = None
    amount: Optional[int] = None
    unit: Optional[str] = None

class MarketplaceSegmentDetail(BaseModel):
    segment_id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    category: Optional[str]
    country_codes: Optional[List[str]]
    currency_codes: Optional[List[str]]
    identifier_types: Optional[List[str]]

    pricing: Optional[List[MarketplacePricing]] = None  # ✅ NEW

class MarketplaceSegmentDetailResponse(BaseModel):
    segments: List[MarketplaceSegmentDetail]
    pagination: Pagination
