from enum import Enum
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class SegmentUpdateType(str, Enum):
    AVAILABLE = "AVAILABLE"
    METADATA_UPDATED = "METADATA_UPDATED"
    PARTIAL_REFRESH = "PARTIAL_REFRESH"
    FULL_REFRESH = "FULL_REFRESH"
    UNAVAILABLE = "UNAVAILABLE"
    DELETED = "DELETED"


class SegmentUpdate(BaseModel):
    segmentId: int = Field(
        ...,
        description="LiveRamp marketplace segment ID"
    )

    updatedAt: datetime = Field(
        ...,
        description="Time the update event occurred"
    )

    updateType: SegmentUpdateType = Field(
        ...,
        description="Type of update event emitted by LiveRamp"
    )


class SegmentUpdatesResponse(BaseModel):
    message: Optional[str] = None
    v3_SegmentUpdates: List[SegmentUpdate]
    nextCursor: Optional[str] = None
