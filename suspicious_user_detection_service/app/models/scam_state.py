from typing import List, Optional
from app.models.anomaly import Post 

class ScamState(dict):
    user_id: str
    posts: List[Post]
    suspicious_reasons: List[str]
    suspicious_score: int
    llm_analysis: Optional[dict]