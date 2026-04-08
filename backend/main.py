from fastapi import FastAPI
from pydantic import BaseModel
import requests
from PIL import Image
from io import BytesIO
from transformers import CLIPProcessor, CLIPModel
import torch

app = FastAPI()

# Load model once when server starts
model = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
processor = CLIPProcessor.from_pretrained("patrickjohncyh/fashion-clip")

class PinRequest(BaseModel):
    image_url: str

@app.post("/search")
def search(request: PinRequest):
    # Fetch image from URL
    response = requests.get(request.image_url)
    image = Image.open(BytesIO(response.content))
    
    # Generate embedding
    inputs = processor(images=image, return_tensors="pt")
    embedding = model.vision_model(**inputs).pooler_output

    return {"embedding_shape": list(embedding.shape)}