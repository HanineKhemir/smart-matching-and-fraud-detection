from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, HnswConfigDiff, OptimizersConfigDiff, WalConfigDiff

# Initialize Qdrant client
client = QdrantClient(host="localhost", port=6333, timeout=30)
COLLECTION_NAME = "last_collection"

def initialize_qdrant_collection():
    try:
        # Check if the collection already exists
        existing_collections = [collection.name for collection in client.get_collections().collections]
        if COLLECTION_NAME in existing_collections:
            print(f"Collection '{COLLECTION_NAME}' already exists.")
            return

        # Create the collection if it doesn't exist
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=512,
                distance="Cosine",
                on_disk=False  # Important for reliable storage
            ),
            hnsw_config=HnswConfigDiff(
                m=16,
                ef_construct=100,
                on_disk=False
            ),
            optimizers_config=OptimizersConfigDiff(
                indexing_threshold=10000,
                memmap_threshold=100000
            ),
            wal_config=WalConfigDiff(
                wal_capacity_mb=64
            )
        )
        print(f"Collection '{COLLECTION_NAME}' created successfully.")
    except Exception as e:
        print(f"Error initializing collection '{COLLECTION_NAME}': {e}")
        raise
