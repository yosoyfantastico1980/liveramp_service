# models.py
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ErrorDetail(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: int
    message: str


class ErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    error: ErrorDetail


class Pagination(BaseModel):
    """
    LiveRamp pagination envelope is usually:
      {"after": "...", "total": 348}
    """
    model_config = ConfigDict(extra="allow")
    after: Optional[str] = None
    total: Optional[int] = None


class Destination(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: str
    name: Optional[str] = None
    logoUrl: Optional[str] = None


class DestinationsResponse(BaseModel):
    """
    LiveRamp returns a top-level key literally named 'v2/Destinations'.
    We map that to a pythonic `destinations` field via alias.
    """
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    destinations: List[Destination] = Field(default_factory=list, alias="v2/Destinations")
    pagination: Optional[Pagination] = Field(default=None, alias="_pagination")


class Segment(BaseModel):
    """
    Keep this loose; LiveRamp segment objects can vary by endpoint.
    """
    model_config = ConfigDict(extra="allow")
    id: Optional[str] = None
    name: Optional[str] = None


class SegmentsResponse(BaseModel):
    """
    Segment list key can vary by LiveRamp endpoint/version.
    We'll support the common patterns without you having to be perfect upfront.
    """
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    segments: List[Segment] = Field(default_factory=list, alias="v2/Segments")
    pagination: Optional[Pagination] = Field(default=None, alias="_pagination")

    @model_validator(mode="before")
    @classmethod
    def _coerce_segments_key(cls, data: Any) -> Any:
        """
        If LiveRamp returns segments under a different top-level key,
        normalize it into the alias expected by this model.
        """
        if not isinstance(data, dict):
            return data

        # If v2/Segments exists, nothing to do
        if "v2/Segments" in data:
            return data

        # Common alternates we’ve seen in APIs
        for alt in ("segments", "v2/Segment", "v2/segments", "Segments"):
            if alt in data and "v2/Segments" not in data:
                data["v2/Segments"] = data[alt]
                break

        return data
