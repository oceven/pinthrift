import requests
from bs4 import BeautifulSoup

SUPPORTED_PLATFORMS = ["poshmark", "vinted"]

def is_supported_listing(url):
    return any(platform in url.lower() for platform in SUPPORTED_PLATFORMS)


def get_listing_info(listing_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(listing_url, headers=headers)   
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch listing: {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract info from meta tags
    image_tag = soup.find("meta", property="og:image")
    title_tag = soup.find("meta", property="og:title")
    price_tag = soup.find("meta", property="product:price:amount")
    

    image_url = image_tag["content"] if image_tag else None
    title = title_tag["content"] if title_tag else "Unknown title"
    price = float(price_tag["content"]) if price_tag else 0.0

    return {
        "title": title,
        "image_url": image_url,
        "price": price,
    }
    
def is_pinterest_pin(url):
    return "pinterest.com/pin/" in url

def get_image_from_pin(pin_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(pin_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    image_tag = soup.find("meta", property="og:image")
    return image_tag["content"] if image_tag else None