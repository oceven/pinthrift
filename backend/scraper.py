import requests
from bs4 import BeautifulSoup

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