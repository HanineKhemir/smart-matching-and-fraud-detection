from fastapi import FastAPI
from app.api.v1.endpoints import embeddings 
from app.config.qdrant_config import initialize_qdrant_collection
from app.api.v2.endpoints import embeddings as embeddings_v2

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("Initializing Qdrant collection...")
    initialize_qdrant_collection()
    

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the LostFound AI Service"}

app.include_router(embeddings.router, prefix="/api/v1/embedding")
app.include_router(embeddings_v2.router, prefix="/api/v2/embedding")