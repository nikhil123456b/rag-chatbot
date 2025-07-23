import requests
from bs4 import BeautifulSoup
import os
import json

BASE_URL = "https://www.changiairport.com"

# List of subpages to crawl (you can expand this)
PAGES = [
    "/en/airport-guide.html",
    "/en/maps.html",
    "/en/dining.html",
    "/en/shopping.html",
    "/en/discover/changi-experience.html"
]

def get_page_text(url):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text(separator=' ', strip=True)
        return text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def scrape_changi():
    all_data = {}

    for path in PAGES:
        full_url = BASE_URL + path
        print(f"Scraping: {full_url}")
        text = get_page_text(full_url)
        all_data[full_url] = text

    # Save to data/raw/changi_raw.json
    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/changi_raw.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print("✅ Scraping complete. Data saved to data/raw/changi_raw.json")

if __name__ == "__main__":
    scrape_changi()
