import torch
import clip
from PIL import Image
import io
import numpy as np

# Load model once and reuse
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def create_clip_embedding(image_bytes: bytes | None, text: str | None) -> list[float]:
    """
    Create CLIP embedding from image and/or text with enhanced handling.
    
    Args:
        image_bytes: Binary image data
        text: Text description
        
    Returns:
        Normalized 512-dimensional embedding vector as list of floats
        
    Raises:
        ValueError: If neither image nor text is provided
        RuntimeError: If embedding generation fails
    """
    if not image_bytes and not text:
        raise ValueError("At least one of image or text must be provided")

    try:
        image_feat = None
        text_feat = None
        
        with torch.no_grad():
            # Process image if provided
            if image_bytes:
                try:
                    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
                    image_tensor = preprocess(image).unsqueeze(0).to(device)
                    image_feat = model.encode_image(image_tensor)
                    image_feat /= image_feat.norm(dim=-1, keepdim=True)  # Normalize
                except Exception as e:
                    print(f"Image processing failed: {str(e)}")
                    if not text:
                        raise RuntimeError("Image processing failed and no text provided")

            # Process text if provided
            if text:
                # Truncate input text before tokenization to ~256 characters (safe approx. for 77 tokens)
                max_chars = 256
                truncated_text = text[:max_chars]
                text_tokens = clip.tokenize([truncated_text]).to(device)
                text_feat = model.encode_text(text_tokens)
                text_feat /= text_feat.norm(dim=-1, keepdim=True)  # Normalize

            # Combine features if both exist
            if image_feat is not None and text_feat is not None:
                combined = (image_feat + text_feat) / 2
            else:
                combined = image_feat if image_feat is not None else text_feat

            # Verify output embedding size
            embedding = combined[0].cpu().numpy()
            if embedding.shape[0] != 512:
                raise RuntimeError(f"Unexpected embedding size: {embedding.shape}")

            return embedding.tolist()

    except Exception as e:
        raise RuntimeError(f"Embedding generation failed: {str(e)}") from e
