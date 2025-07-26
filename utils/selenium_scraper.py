from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import time

def setup_browser():
    options = Options()
    options.add_argument("--headless=new")  # modern headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_terminal_dining(terminal_url: str, terminal_name: str):
    driver = setup_browser()
    print(f"🔍 Scraping {terminal_name} from: {terminal_url}")
    driver.get(terminal_url)
    time.sleep(3)  # wait for JS to load

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    results = []
    for marker in soup.find_all("div", class_="poi-info"):
        name = marker.find("div", class_="poi-title")
        category = marker.find("div", class_="poi-category")
        if name:
            results.append({
                "terminal": terminal_name,
                "name": name.text.strip(),
                "category": category.text.strip() if category else "Unknown"
            })

    return results

if __name__ == "__main__":
    urls = {
        "T1": "https://www.changiairport.com/en/maps/terminal-1.html",
        "T2": "https://www.changiairport.com/en/maps/terminal-2.html",
        "T3": "https://www.changiairport.com/en/maps/terminal-3.html",
        "T4": "https://www.changiairport.com/en/maps/terminal-4.html"
    }

    all_data = []
    for terminal, url in urls.items():
        data = scrape_terminal_dining(url, terminal)
        all_data.extend(data)

    with open("data/raw/terminal_dining.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print("✅ Scraping completed and saved to data/raw/terminal_dining.json")
