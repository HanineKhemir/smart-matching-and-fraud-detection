from fastapi import HTTPException
from app.services.clip_service import create_clip_embedding
from app.services.vector_service import qdrant_delete, qdrant_store, qdrant_search
from qdrant_client.http.exceptions import ResponseHandlingException
from app.config.qdrant_config import client, COLLECTION_NAME
from app.config.config import PROXY_API_KEY, PROXY_BASE_URL
import requests
import uuid

def generate_embedding(image_name: str, text: str):

    image_bytes = None

    if image_name:  
        image_url = f"{PROXY_BASE_URL}/download/{image_name}"
        headers = {"X-API-Key": PROXY_API_KEY}
        response = requests.get(image_url, headers=headers)
        response.raise_for_status()
        image_bytes = response.content

    return create_clip_embedding(image_bytes, text)

def store_embedding(post_id: str, embedding, metadata: dict) -> bool:
    try:
        return qdrant_store(post_id, embedding, metadata)
    except Exception as e:
        print(f"Error in store_embedding: {e}")
        return False

def find_similar_embeddings(post_id :str):
   return qdrant_search(post_id)

def delete_embedding(post_ids: str):
    return qdrant_delete([post_ids])

