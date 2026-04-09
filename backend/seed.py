from database import SessionLocal, Listing
from transformers import CLIPProcessor, CLIPModel
from PIL import Image

model = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
processor = CLIPProcessor.from_pretrained("patrickjohncyh/fashion-clip")

def get_embedding(path):
    image = Image.open(path)
    inputs = processor(images=image, return_tensors="pt")
    embedding = model.vision_model(**inputs).pooler_output
    return embedding.detach().numpy().squeeze().tolist()

listings_data = [
    {"title": "Top 1", "price": 25, "platform": "Depop", "link": "https://depop.com/fake1", "image_url": "top.jpg", "image_path": "top.jpg"},
    {"title": "Top 2", "price": 30, "platform": "Vinted", "link": "https://vinted.com/fake2", "image_url": "top2.jpg", "image_path": "top2.jpg"},
    {"title": "Skirt", "price": 15, "platform": "eBay", "link": "https://ebay.com/fake3", "image_url": "skirt.jpg", "image_path": "skirt.jpg"},
    {"title": "Top 3", "price": 20, "platform": "Depop", "link": "https://depop.com/fake4", "image_url": "top3.jpg", "image_path": "top3.jpg"},
    {"title": "Top 5", "price": 18, "platform": "Vinted", "link": "https://vinted.com/fake5", "image_url": "top5.jpg", "image_path": "top5.jpg"},
]

db = SessionLocal()
print("Connected to database")

for item in listings_data:
    print(f"Processing {item['title']}...")
    embedding = get_embedding(item["image_path"])
    print(f"Got embedding for {item['title']}")
    listing = Listing(
        title=item["title"],
        price=item["price"],
        platform=item["platform"],
        link=item["link"],
        image_url=item["image_url"],
        embedding=embedding
    )
    db.add(listing)
    print(f"Added {item['title']} to session")

db.commit()
print("Committed!")
db.close()
print("Database seeded successfully!")