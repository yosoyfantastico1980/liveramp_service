from typing import Optional
from fastapi import APIRouter, Query
from models.segment_updates import SegmentUpdatesResponse
from app.main import lr_request

router = APIRouter(
    prefix="/v1",
    tags=["Segment Updates"],
)


@router.get(
    "/segment-updates",
    response_model=SegmentUpdatesResponse,
    summary="Retrieve marketplace segment update events",
)
def get_segment_updates(
    since: str = Query(
        ...,
        description="ISO timestamp to retrieve updates since",
    ),
    cursor: Optional[str] = Query(
        None,
        description="Pagination cursor returned from previous call",
    ),
):
    qp = {"since": since}
    if cursor:
        qp["cursor"] = cursor

    upstream = lr_request(
        "GET",
        "/data-marketplace/buyer-api/v3/segment-updates",
        None,
        query_params=qp,
    )

    return upstream
