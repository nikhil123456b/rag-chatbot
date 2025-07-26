from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import os

# Terminal-specific URLs
TERMINAL_URLS = {
    "T1": "https://www.changiairport.com/en/dine-and-shop/dining-directory.html?location=t1",
    "T2": "https://www.changiairport.com/en/dine-and-shop/dining-directory.html?location=t2",
    "T3": "https://www.changiairport.com/en/dine-and-shop/dining-directory.html?location=t3",
    "T4": "https://www.changiairport.com/en/dine-and-shop/dining-directory.html?location=t4",
    "Jewel": "https://www.changiairport.com/en/dine-and-shop/dining-directory.html?location=j1",
}

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def extract_data(html):
    soup = BeautifulSoup(html, "html.parser")
    print("📄 Preview of HTML:", soup.prettify()[:2000])  # print first 2k characters
    cards = soup.select("div.dine-shop-card")
    results = []

    for card in cards:
        name = card.select_one(".name")
        category = card.select_one(".category")
        location = card.select_one(".location")
        time_elem = card.select_one(".time")

        results.append({
            "name": name.get_text(strip=True) if name else "N/A",
            "category": category.get_text(strip=True) if category else "N/A",
            "location": location.get_text(strip=True) if location else "N/A",
            "hours": time_elem.get_text(strip=True) if time_elem else "N/A"
        })

    return results

def scrape_all():
    driver = setup_driver()
    os.makedirs("data/structured", exist_ok=True)

    for terminal, url in TERMINAL_URLS.items():
        print(f"🔍 Scraping {terminal}...")
        driver.get(url)
        time.sleep(15)  # wait for JS to load

        html = driver.page_source
        listings = extract_data(html)

        # Save to file
        output_file = f"data/structured/{terminal.lower()}_dining.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(listings, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved {len(listings)} listings for {terminal} → {output_file}\n")

    driver.quit()

if __name__ == "__main__":
    scrape_all()
