from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from typing import Literal, List


class PricingSegment(BaseModel):
    id: str
    name: str
    status: Literal["active", "inactive", "archived"]
    base_cpm: Decimal
    currency: str
    data_source: str
    created_at: datetime
    updated_at: datetime


class BulkReconciliationRequest(BaseModel):
    segment_ids: List[str] = Field(
        ...,
        example=[
            "1044434333",
            "1015273111",
            "1590000000"
        ]
    )


from pydantic import BaseModel
from datetime import date
from typing import List


class PriceChangeEvent(BaseModel):
    segment_id: int
    segment_name: str
    day: date
    new_price: float
    old_price: float


class PriceChangeResponse(BaseModel):
    source: str
    count: int
    results: List[PriceChangeEvent]
