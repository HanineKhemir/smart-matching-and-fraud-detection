import base64
from fastapi import APIRouter, File, Form, UploadFile
from app.models.anomaly import Post, userPosts, AnomalyResponse
from app.services.scam_detector_agent import scam_detector_agent
from app.config.redis_client import redis_client, test_redis
from app.repositories.redis_repo import test

router = APIRouter()

@router.post("/detect")
async def detect_suspicious_user(
    user_id: str = Form(...),
    post_id: str = Form(...),
    post_type: str = Form(...),
    text: str = Form(...),
    date: str = Form(...),  # Assuming date is passed as a string
    item_type: str = Form(...),
    image_file: UploadFile = File(...)):

    image_content = await image_file.read()
    image_base64 = base64.b64encode(image_content).decode("utf-8")

    post = Post(
        userid=user_id,
        postid=post_id,
        posttype=post_type,
        date=date,
        text=text,
        itemtype=item_type,
        imagefile=image_base64
    )

    return await  scam_detector_agent(post)

@router.get("/test_redis/")
async def get_key():
    try:
        return await test_redis()
    except Exception as e:
        return {"error": str(e)}

@router.get("/test_repo/")
async def test_repo():
    try:
        await test()
    except Exception as e:
        return {"error": str(e)}