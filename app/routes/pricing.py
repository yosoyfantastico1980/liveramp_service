from fastapi import APIRouter, HTTPException
from app.services.pricing_service import get_pricing_segment

router = APIRouter(prefix="/v1/pricing", tags=["pricing"])


@router.get("/segments/{segment_id}")
async def fetch_pricing_segment(segment_id: str):
    segment = await get_pricing_segment(segment_id)

    if not segment:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "SEGMENT_NOT_FOUND",
                "message": f"Segment {segment_id} not found",
            },
        )

    return segment
