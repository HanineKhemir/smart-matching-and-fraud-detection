from fastapi import APIRouter, HTTPException
from app.api.v1.dependencies import delete_embedding, generate_embedding, store_embedding, find_similar_embeddings
from app.models.embedding_request import EmbeddingRequest
from app.services.vector_service import client
#from app.services.vector_service import get_embedding_by_post_id
from app.config.qdrant_config import client, COLLECTION_NAME
import numpy as np

router = APIRouter()

# @router.post("/generate")
# async def generate_embedding_endpoint(req: EmbeddingRequest):
#     """Enhanced endpoint with better error handling"""
#     try:
#         embedding = generate_embedding(req.image_url, req.text)
#         if not isinstance(embedding, (list, np.ndarray)) or len(embedding) != 512:
#             raise ValueError(f"Invalid embedding: type={type(embedding)}, len={len(embedding)}")
#         metadata = req.dict()
#         print(f"Storing embedding for post_id={req.post_id}")
#         store_result = store_embedding(req.post_id, embedding, metadata)
#         print(f"Store result: {store_result}")
        
#         if not store_result:
#             raise RuntimeError("Storage verification failed")
            
#         return {
#             "status": "success",
#             "post_id": req.post_id,
#             "vector_length": len(embedding)
#         }
        
#     except Exception as e:
#         print(f"Error in /generate endpoint: {e}")
#         raise HTTPException(
#             status_code=500,
#             detail=f"Failed: {str(e)}"
#         )


@router.get("/similar/{post_id}")
async def get_similar(post_id: str):
    results = find_similar_embeddings(post_id)
    return {"results": results}

@router.delete("/delete/{post_id}")
async def delete_embeddings(post_id: str):
    return delete_embedding(post_id)

# for development purposes only

@router.get("/check_collection")
def check_collection():
    try:
        collections = client.get_collections()
        return [collection.name for collection in collections.collections]
    except Exception as e:
        print(f"Error checking collections: {e}")
        return {"error": str(e)}


@router.get("/get_all_points")
def get_all_points():
    try:
        points = []
        offset = 0
        limit = 100  # Number of points to retrieve per batch

        while True:
            result = client.scroll(
                collection_name=COLLECTION_NAME,
                limit=limit,
                offset=offset
            )
            points.extend(result[0])  # Add the retrieved points to the list
            offset += len(result[0])  # Increment the offset by the number of points retrieved

            if len(result[0]) < limit:  # Stop if fewer points than the limit are returned
                break

        return [{"id": point.id, "vector": point.vector, "payload": point.payload} for point in points]
    except Exception as e:
        print(f"Error retrieving points from Qdrant: {e}")
        return {"error": str(e)}


@router.get("/collection_info")
async def get_collection_info():
    """Get detailed collection configuration"""
    try:
        info = client.get_collection(COLLECTION_NAME)
        return {
            "status": "success",
            "config": info.config.dict(),
            "vectors_count": info.vectors_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/verify_storage/{post_id}")
async def verify_storage(post_id: str):
    try:
        result = client.retrieve(
            collection_name=COLLECTION_NAME,
            ids=[int(post_id) if post_id.isdigit() else post_id],
            with_vectors=True
        )
        
        if not result:
            return {"stored": False, "error": "Point not found"}
            
        return {
            "stored": True,
            "has_vector": result[0].vector is not None,
            "vector_length": len(result[0].vector) if result[0].vector else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

        
# @router.get("/get_embedding/{post_id}")
# async def get_embedding(post_id: str):
#     try:
#         embedding = get_embedding_by_post_id(post_id)
#         if embedding:
#             return {"post_id": post_id, "embedding": embedding}
#         else:
#             return {"post_id": post_id, "error": "No embedding found"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))