from database import SessionLocal, Listing
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
from io import BytesIO
import requests
from scraper import get_listing_info


model = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
processor = CLIPProcessor.from_pretrained("patrickjohncyh/fashion-clip")

def get_embedding_from_url(image_url):
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    inputs = processor(images=image, return_tensors="pt")
    embedding = model.vision_model(**inputs).pooler_output
    return embedding.detach().numpy().squeeze().tolist()

# Just listing URLs and platform — everything else is scraped automatically
listings_data = [
    {"url": "https://poshmark.ca/listing/Last-Kiss-Y2K-Brown-and-White-Herringbone-Coat-69aca2bbdc3b4666d81e823c", "platform": "Poshmark"},
    {"url": "https://poshmark.ca/listing/GAP-Navy-DoubleBreasted-Peacoat-Jacket-Womens-Size-Medium-69c2dd4d310f1c495d6b453f", "platform": "Poshmark"},
    {"url": "https://poshmark.ca/listing/Jones-New-York-Blouse-69ca8dc7ef1ef71a75ac4dbb", "platform": "Poshmark"},
    {"url": "https://poshmark.ca/listing/Vintage-White-Crochet-Mini-Dress-with-VNeck-69cc0a8849e17bd6b1eb1be0", "platform": "Poshmark"},
    {"url": "https://poshmark.ca/listing/Rebellion-White-Lace-Camisole-Top-Small-69c6b42f00d0288b254576f4", "platform": "Poshmark"},
    {"url": "https://poshmark.ca/listing/Rebellion-Light-Blue-LaceTrim-Spaghetti-Strap-Camisole-Babydoll-69c47e422fa054d92a9450ca", "platform": "Poshmark"},
    {"url": "https://poshmark.ca/listing/Aritzia-Red-SpaghettiStrap-TieFront-Camisole-69af3ae0b6af92d6f7db9e26", "platform": "Poshmark"},
    {"url": "https://poshmark.ca/listing/WILFRED-Amore-Camisole-69bfef25fe4c68b8c2bc0348", "platform": "Poshmark"},
    {"url": "https://poshmark.ca/listing/Abercrombie-Fitch-Black-Womens-Mini-Skirt-69d55cbe05deb30279bd222e", "platform": "Poshmark"},
    {"url": "https://poshmark.ca/listing/holdsteal-authentic-CHANEL-Black-and-White-Tweed-Dress-with-Gold-Accents-69bca207149377607850837f", "platform": "Poshmark"},
    {"url": "https://poshmark.ca/listing/Vintage-Y2K-Elegant-Babydoll-Top-with-Lace-and-Bow-69c9ec793509d12914203824", "platform": "Poshmark"},
    {"url": "https://poshmark.ca/listing/Vivienne-Westwood-Black-Heart-Crossbody-Bag-68fd07cc955383fc0855dde8", "platform": "Poshmark"},
    {"url": "https://poshmark.ca/listing/Jirai-Kei-Purple-Pink-Jfashion-Blouse-698eb0abb09b7c083d059644", "platform": "Poshmark"},
    {"url": "https://poshmark.ca/listing/Lolita-JSK-and-Cardigan-With-Flower-Details-69d58d28d8024c9c7ae3612a", "platform": "Poshmark"},
    # add more...
]

db = SessionLocal()
db.query(Listing).delete()
db.commit()
print("Cleared existing listings")

for item in listings_data:
    print(f"Processing {item['url']}...")
    try:
        info = get_listing_info(item["url"])
        embedding = get_embedding_from_url(info["image_url"])
        listing = Listing(
            title=info["title"],
            price=info["price"],
            platform=item["platform"],
            link=item["url"],
            image_url=info["image_url"],
            embedding=embedding
        )
        db.add(listing)
        print(f"✓ {info['title']} — ${info['price']}")
    except Exception as e:
        print(f"✗ Failed: {e}")

db.commit()
db.close()
print("Done!")