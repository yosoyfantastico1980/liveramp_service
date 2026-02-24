from fastapi import APIRouter

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])

@router.post("/")
def create_onboarding(payload: dict):
    return {
        "message": "Onboarding request received",
        "payload": payload
    }

