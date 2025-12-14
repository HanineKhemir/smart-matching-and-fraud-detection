import base64
import requests
from PIL import Image
import io
import imagehash
import re
from collections import Counter
from typing import List, Optional
from app.models.anomaly import Post
from app.config.config import PROXY_BASE_URL, PROXY_API_KEY
from app.repositories.redis_repo import add_to_set, is_member_of_set,increment_id_key

async def check_duplicate_images(post: Post) -> Optional[str]:
    """Detect if the user has posted the same image more than once (by perceptual hash)."""
    if post.imagefile:
            try:
                image_bytes = base64.b64decode(post.imagefile)
                image = Image.open(io.BytesIO(image_bytes))
                img_hash = str(imagehash.phash(image))
                if await add_to_set(f"{post.userid}_image_hashes", img_hash)==0:
                    print("duplicate image detected")
                    return f"Duplicate image detected in posts for user {post.userid}"
            except Exception as e:
                print(f"Error processing image for user {post.userid}: {e}")
    return None

async def check_links(post: Post) -> Optional[str]:
    link_pattern = re.compile(r"(https?://\S+|www\.\S+)", re.IGNORECASE)
    if post.text and link_pattern.search(post.text):
            flaggedposts = await increment_id_key(f"{post.userid}_external_links", 86400*30)
            return (f"External link detected in post {post.postid}")
  
    return None

async def check_post_frequency(post: Post) -> Optional[str]:
    try :
        """Detect if user made 3 or more posts in a single day."""
        if int(await increment_id_key(f"{post.userid}_daily_posts", 86400)) >= 3:
            return f"User {post.userid} has made 3 or more posts in a single day."
        return None
    except Exception as e:
        print(f"Error checking post frequency for user {post.userid}: {e}")
        return None
