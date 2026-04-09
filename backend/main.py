from fastapi import FastAPI, Depends
from pydantic import BaseModel
import requests
from PIL import Image
from io import BytesIO
from transformers import CLIPProcessor, CLIPModel
import faiss
import numpy as np
from sqlalchemy.orm import Session
from database import get_db, Listing

app = FastAPI()

# Load model once when server starts
model = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
processor = CLIPProcessor.from_pretrained("patrickjohncyh/fashion-clip")

# Generate embedding from a local image file
def get_embedding(path):
    image = Image.open(path)
    inputs = processor(images=image, return_tensors="pt")
    embedding = model.vision_model(**inputs).pooler_output
    return embedding.detach().numpy()

def build_index(db: Session):
    listings = db.query(Listing).all()
    if not listings:
        return None, []
    
    embeddings = np.array([l.embedding for l in listings]).astype("float32")
    faiss.normalize_L2(embeddings)
    
    index = faiss.IndexFlatIP(768)
    index.add(embeddings)
    return index, listings

class PinRequest(BaseModel):
    image_url: str

@app.post("/search")
def search(request: PinRequest, db: Session = Depends(get_db)):
    # Build index from database
    index, listings = build_index(db)
    
    if not listings:
        return {"results": [], "message": "No listings in database yet"}

    # Fetch image from URL
    response = requests.get(request.image_url)
    image = Image.open(BytesIO(response.content))

    # Generate embedding
    inputs = processor(images=image, return_tensors="pt")
    embedding = model.vision_model(**inputs).pooler_output

    # Convert to numpy for FAISS
    query = embedding.detach().numpy().astype("float32")
    faiss.normalize_L2(query)

    # Search top 3 matches
    distances, indices = index.search(query, k=3)

    # Build results
    results = []
    for i, idx in enumerate(indices[0]):
        listing = listings[idx]
        results.append({
            "id": listing.id,
            "title": listing.title,
            "price": listing.price,
            "platform": listing.platform,
            "link": listing.link,
            "image_url": listing.image_url,
            "similarity": round(float(distances[0][i]), 4)
        })

    return {"results": results}