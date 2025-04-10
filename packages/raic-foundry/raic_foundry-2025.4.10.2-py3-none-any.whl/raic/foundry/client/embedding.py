import io
import base64
import pickle
from PIL import Image
from .request import raic_get, raic_upload_file
from .raic_client_base import RaicClient

class EmbeddingClient(RaicClient):
    def __init__(self):
        return super().__init__()
    
    def upload_image(self, image: Image.Image, vectorizer_model_id: str):
        request = f"cascade-vision/external/upload"
        query_params = { 'embedder_id': vectorizer_model_id }

        byte_stream = io.BytesIO()
        image.save(byte_stream, format='JPEG')
        byte_stream.seek(0)

        return raic_upload_file(request, image.filename, byte_stream, content_type='image/jpeg', query_params=query_params)

    def get_image_detection_info(self, detection_id: str, include_embedding: bool=False):
        request = f"cascade-vision/external/{detection_id}"
        query_params = { 'include_embeddings': include_embedding }
        return raic_get(request, query_params=query_params)



