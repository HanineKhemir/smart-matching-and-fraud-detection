from pydantic import BaseModel
from typing import Literal, Optional

class EmbeddingRequest(BaseModel):
    post_id: str
    post_type: Literal["lostitem", "founditem"]  # validates only these two values
    image_url: Optional[str]  # Make image_url optional
    text: str
    item_type: str
    