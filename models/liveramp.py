from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class Destination(BaseModel):
    """
    Stable representation of a LiveRamp destination
    exposed through our v1 API.
    """
    id: str
    name: str
    logo_url: Optional[str] = None


class Pagination(BaseModel):
    after: Optional[str] = Field(
        default=None,
        example="eyJ2ZXJzaW9uIjoxLCJvZmZzZXQiOjF9",
        description="Cursor token for retrieving next page"
    )

    total: Optional[int] = Field(
        default=None,
        example=6,
        description="Total number of records returned"
    )


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

    description: Optional[str] = None
    segmentType: Optional[str] = None
    providerComments: Optional[str] = None
    identifierType: Optional[str] = None
    updatedAt: Optional[str] = None

    # Nested fields simplified
    countryCode: Optional[str] = None
    location: Optional[str] = None

    # Pricing (simplified to main USD targeting price)
    digitalAdTargetingPriceUSD: Optional[int] = None



class MarketplaceSegmentListResponse(BaseModel):
    segments: List[MarketplaceSegment]
    pagination: Pagination

from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class IdentifierType(str, Enum):
    COOKIE = "COOKIE"
    MAID = "MAID"
    CTV = "CTV"
    EMAIL = "EMAIL"


class RequestedSegmentInput(BaseModel):
    segment_id: int = Field(..., description="LiveRamp segment ID")
    destination_id: int = Field(..., description="LiveRamp destination ID")
    identifier_type: Optional[IdentifierType] = Field(
        None,
        description="Identifier type used for activation"
    )

class RequestedSegmentsRequest(BaseModel):
    segments: List[RequestedSegmentInput]

model_config = {
    "json_schema_extra": {
        "example": {
            "segments": [
                {
                    "segment_id": 1012603801,
                    "destination_id": 16859,
                    "identifier_type": "COOKIE"
                }
            ]
        }
    }
}


class RequestedSegmentResult(BaseModel):
    segment_id: Optional[int] = None
    request_id: Optional[str] = None
    status: Optional[str] = None


class RequestedSegmentsResponse(BaseModel):
    results: List[RequestedSegmentResult]

from enum import Enum

class SegmentType(str, Enum):
    DATA_MARKETPLACE = "DATA_MARKETPLACE"
    ONBOARDING = "ONBOARDING"


class ActivationState(str, Enum):
    """
    Normalized activation state across LiveRamp segment types.
    """

    ACTIVE = "ACTIVE"
    """
    Segment is successfully delivered and active at the destination.
    """

    PENDING = "PENDING"
    """
    Segment activation request has been received but is not yet fully processed.
    """

    FAILED = "FAILED"
    """
    Activation attempt failed at LiveRamp or destination.
    """

    UNKNOWN = "UNKNOWN"
    """
    Activation state could not be determined.
    Typically returned when no destination match exists.
    """


class SegmentStatus(BaseModel):
    segment_id: int = Field(
        example=1015271391,
        description="LiveRamp segment ID"
    )

    destination_id: Optional[str] = Field(
        None,
        example="cf46086e-df54-47f5-83b8-8115642c75c4",
        description="LiveRamp destination UUID"
    )

    activation_state: ActivationState = Field(
        example="ACTIVE",
        description="Normalized activation state of the segment at the destination"
    )

class Pagination(BaseModel):
    after: Optional[str] = None
    total: int


class SegmentStatusListResponse(BaseModel):
    statuses: List[SegmentStatus]
    pagination: Pagination



class CountryCode(str, Enum):
    USA = "USA"


class CurrencyCode(str, Enum):
    USD = "USD"


class Delivery(BaseModel):
    delivery_id: Optional[str] = None
    segment_id: Optional[int] = None
    device_type: Optional[str] = None
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

# ==============================
# First Party Distribution
# ==============================

class FirstPartyDistributionInput(BaseModel):
    segment_id: int = Field(..., description="First-party segment ID")
    destination_id: int = Field(..., description="LiveRamp destination ID")
    identifier_type: Optional[IdentifierType] = Field(
        None,
        description="Identifier type used for distribution"
    )


class FirstPartyDistributionRequest(BaseModel):
    segments: List[FirstPartyDistributionInput]

    model_config = {
        "json_schema_extra": {
            "example": {
                "segments": [
                    {
                        "segment_id": 123456789,
                        "destination_id": 16859,
                        "identifier_type": "COOKIE"
                    }
                ]
            }
        }
    }


class FirstPartyDistributionResult(BaseModel):
    segment_id: int
    destination_id: Optional[int] = None  # ✅ make optional
    status: str
    distribution_id: Optional[str] = None

class FirstPartyDistributionResponse(BaseModel):
    results: List[FirstPartyDistributionResult]

class PricingSource(str, Enum):
    LIVERAMP = "LIVERAMP"
    PULSEPOINT = "PULSEPOINT"


class SegmentPricingRecord(BaseModel):
    source: PricingSource
    effective_date: str
    use_case: Optional[str] = None
    currency_code: Optional[str] = None
    amount: Optional[int] = None
    unit: Optional[str] = None


class SegmentPricingHistoryResponse(BaseModel):
    segment_id: int
    pricing_history: List[SegmentPricingRecord]

