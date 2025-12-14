from fastapi import FastAPI
from app.api.v1.endpoints import anomalydetection
from app.api.v2.endpoints import anomalydetection as anomalydetection_v2

app = FastAPI()


    

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the suspicious_user_detection_service AI Service"}

app.include_router(anomalydetection.router, prefix="/api/v1/anomalydetection")
app.include_router(anomalydetection_v2.router, prefix="/api/v2/anomalydetection")