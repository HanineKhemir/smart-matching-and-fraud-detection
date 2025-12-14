from fastapi import APIRouter
from app.models.anomaly import userPosts, AnomalyResponse
from app.services.scam_detector_agent import scam_detector_agent

router = APIRouter()

@router.post("/detect", response_model=AnomalyResponse)
async def detect_suspicious_user(user_posts: userPosts):
    return scam_detector_agent(user_posts)
