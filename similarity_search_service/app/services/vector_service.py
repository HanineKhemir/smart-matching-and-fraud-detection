from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, HnswConfigDiff, OptimizersConfigDiff, WalConfigDiff
from qdrant_client.models import FieldCondition, Match, Filter
from app.models.embedding_request import EmbeddingRequest
from typing import List
from qdrant_client.models import PointsSelector, PointIdsList
from app.config.qdrant_config import client, COLLECTION_NAME
import uuid
import numpy as np
import time
from app.repositories.neo4j_repository import create_similarity_relationship, delete_post


def safe_post_id(post_id: str):
    if post_id.isdigit():
        return int(post_id)
    try:
        return str(uuid.UUID(post_id))
    except (ValueError, AttributeError, TypeError):
        # Generate a deterministic UUID from the string
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, post_id))

def qdrant_store(post_id, embedding, metadata: dict) -> bool:
    """Enhanced storage with validation"""
    try:
        if isinstance(embedding, np.ndarray):
            embedding = embedding.astype(np.float32).tolist()  # Force 32-bit floats
        elif isinstance(embedding, list):
            embedding = [float(x) for x in embedding]
        else:
            raise ValueError(f"Invalid embedding type: {type(embedding)}")

        if len(embedding) != 512:
            raise ValueError(f"Invalid embedding size: {len(embedding)}")

        point = PointStruct(
            id=safe_post_id(post_id),
            vector=embedding,
            payload={**metadata, "original_post_id": post_id}
        )

        for attempt in range(3):
            try:
                print(f"Attempt {attempt + 1}")
                client.upsert(
                    collection_name=COLLECTION_NAME,
                    points=[point],
                    wait=True
                )
                
                stored = client.retrieve(
                    collection_name=COLLECTION_NAME,
                    ids=[point.id],
                    with_vectors=True
                )

                if stored and stored[0].vector:
                    print("Storage verification succeeded.")
                    return True
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == 2:  # Last attempt
                    raise
                time.sleep(0.5 * (attempt + 1))
        
        raise RuntimeError("Storage verification failed after retries")
        
    except Exception as e:
        print(f"Storage failed: {type(e).__name__}: {str(e)}")
        raise

def qdrant_search(post_id: str, filter_keys: List[str] = ["item_type", "post_type"]):
    try:
        """Search for similar embeddings based on a post_id."""

        qdrant_post_id = safe_post_id(post_id)

        original = client.retrieve(collection_name=COLLECTION_NAME, ids=[qdrant_post_id], with_vectors=True)
        if not original:
            print(f"Post ID {post_id} not found in Qdrant.")
            return []

        embedding = original[0].vector
        if embedding is None:
            print(f"No embedding found for Post ID {post_id}.")
            return []

        metadata = original[0].payload

        # Build dynamic filter from existing metadata keys
        conditions = []
        for key in filter_keys:
            if key in metadata:
                if key == "post_type":

                    post_type_values = EmbeddingRequest.__fields__["post_type"].annotation.__args__
                    # Dynamically use the opposite post_type
                    if metadata[key] == post_type_values[0]:  # "lostitem"
                        #conditions.append(FieldCondition(key=key, match=Match(value=EmbeddingRequest.__fields__["post_type"].type.__args__[1])))   "founditem"
                        conditions.append({"key" : key, "match": {"value": post_type_values[1]} })

                    elif metadata[key] == post_type_values[1]:  # "founditem"
                        #conditions.append(FieldCondition(key=key, match=Match(value=EmbeddingRequest.__fields__["post_type"].type.__args__[0])))  "lostitem"
                        conditions.append({"key" : key, "match": {"value": post_type_values[0]}})
                        
                else:
                    # General case for other metadata keys
                    #conditions.append(FieldCondition(key=key, match=Match(value=metadata[key])))
                    conditions.append({"key":key, "match": {"value": metadata[key]}})

        q_filter = Filter(must=conditions) if conditions else None

        results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=embedding,
            limit=2,  # Number of similar items to return
            query_filter=q_filter
        )

        for hit in results:
            create_similarity_relationship(post_id, hit.payload.get("original_post_id", hit.id))

        return [hit.payload.get("original_post_id", hit.id) for hit in results]

    except ValueError as e:
        print(f"Invalid post_id format: {post_id}. Must be an integer or UUID.")
        return []
    except Exception as e:
        print(f"Error searching for similar embeddings: {e}")
        return []
    

def qdrant_delete(post_ids: list[str]):
    """Delete embeddings by a list of post IDs."""
    try:
        post_ids = [int(post_id) if post_id.isdigit() else str(uuid.UUID(post_id)) for post_id in post_ids]
        for post_id in post_ids:
            delete_post(post_id)
        result = client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=PointIdsList(points=post_ids),
            wait=True
        )
        return {
            "status": "success",
            "message": f"Deleted embeddings with post_ids={post_ids}",
        }
    except Exception as e:
        print(f"Error deleting embeddings: {e}")
        return {
            "status": "error",
            "message": str(e)
        }