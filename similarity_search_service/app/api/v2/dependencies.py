from fastapi import HTTPException
from app.services.clip_service import create_clip_embedding
from app.services.vector_service import qdrant_delete, qdrant_store, qdrant_search

def generate_embedding(image_name: str, text: str):

    return create_clip_embedding(image_name, text)

def store_embedding(post_id: str, embedding, metadata: dict) -> bool:
    try:
        return qdrant_store(post_id, embedding, metadata)
    except Exception as e:
        print(f"Error in store_embedding: {e}")
        return False

def find_similar_embeddings(post_id :str):
   return qdrant_search(post_id)

def delete_embedding(post_ids: str):
    return qdrant_delete(post_ids)

