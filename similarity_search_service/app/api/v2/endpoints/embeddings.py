from typing import List
from fastapi import APIRouter, HTTPException, Query
from app.api.v2.dependencies import delete_embedding, generate_embedding, store_embedding, find_similar_embeddings
from app.repositories.neo4j_repository import delete_post, get_similar_posts
from app.services.vector_service import client
#from app.services.vector_service import get_embedding_by_post_id
import numpy as np
from fastapi import APIRouter, Form, UploadFile, File
from fastapi import Form, File, UploadFile

router = APIRouter()

@router.post("/generate")
async def generate_embedding_endpoint(
    post_id: str = Form(...),
    post_type: str = Form(...),
    text: str = Form(...),
    item_type: str = Form(...),
    image_file: UploadFile = File(...)
):
    """Enhanced endpoint with better error handling"""
    try:
        image_bytes = await image_file.read()

        # # Save the image to disk temporarily
        # with open(f"received_image_{post_id}.jpg", "wb") as f:
        #     f.write(image_bytes)

        # # Now you can verify the saved image file manually
        # print(f"Image saved as received_image_{post_id}.jpg")

        embedding = generate_embedding(image_bytes, text)
        if not isinstance(embedding, (list, np.ndarray)) or len(embedding) != 512:
            raise ValueError(f"Invalid embedding: type={type(embedding)}, len={len(embedding)}")
        metadata = {
            "post_id": post_id,
            "post_type": post_type,
            "item_type": item_type
        }
        print(f"Storing embedding for post_id={post_id}")
        store_result = store_embedding(post_id, embedding, metadata)
        print(f"Store result: {store_result}")
        
        if not store_result:
            raise RuntimeError("Storage verification failed")

        results = find_similar_embeddings(post_id)
        return {
            "id": post_id,
            "results": results
            }
        
    except Exception as e:
        print(f"Error in /generate endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed: {str(e)}"
        )

@router.get("/similar/{post_id}")
def similar_posts(post_id: str):
    similar = get_similar_posts(post_id)
    return {"similar_posts": similar}


@router.delete("/delete")
def remove_multiple_posts(post_ids: List[str] = Query(...)):
    return delete_embedding(post_ids)