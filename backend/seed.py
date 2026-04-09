from database import SessionLocal, Listing
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
from io import BytesIO
import requests

model = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
processor = CLIPProcessor.from_pretrained("patrickjohncyh/fashion-clip")

def get_embedding_from_url(image_url):
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    inputs = processor(images=image, return_tensors="pt")
    embedding = model.vision_model(**inputs).pooler_output
    return embedding.detach().numpy().squeeze().tolist()

listings_data = [
    {
        "title": "Brown 70s corduroy jacket",
        "price": 35,
        "platform": "Depop",
        "link": "https://depop.com/products/someitem",
        "image_url": "https://img.depop.com/someimage.jpg",
    },
    # add more listings here...
]

db = SessionLocal()

# Clear existing listings first
db.query(Listing).delete()
db.commit()
print("Cleared existing listings")

for item in listings_data:
    print(f"Processing {item['title']}...")
    try:
        embedding = get_embedding_from_url(item["image_url"])
        listing = Listing(
            title=item["title"],
            price=item["price"],
            platform=item["platform"],
            link=item["link"],
            image_url=item["image_url"],
            embedding=embedding
        )
        db.add(listing)
        print(f"✓ Added {item['title']}")
    except Exception as e:
        print(f"✗ Failed {item['title']}: {e}")

db.commit()
db.close()
print("Done! Database seeded.")