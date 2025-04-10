import io
import numpy as np
from PIL import Image
from typing import Optional
from pathlib import Path
from raic.foundry.client.embedding import EmbeddingClient
from raic.foundry.models import VectorizerModel

def create_embedding(
    image: Image.Image | Path | str, 
    vectorizer_model: Optional[VectorizerModel|str] = 'baseline'
) -> np.ndarray:

    if not isinstance(image, Image.Image):
        image = Image.open(str(Path(image)))

    if isinstance(vectorizer_model, str):
        vectorizer_model = VectorizerModel.from_existing(vectorizer_model)

    with image:
        result = EmbeddingClient().upload_image(image, vectorizer_model.id)

    detection_info = EmbeddingClient().get_image_detection_info(result['detectionId'], include_embedding=True)

    return np.array(detection_info['embedding'])