import requests
import json
import os

TERMINALS = ["t1", "t2", "t3", "t4", "j1"]
LIMIT = 15  # results per request

def scrape_terminal_shopping(terminal):
    print(f"\n🛍️ Scraping Shopping – {terminal.upper()}")
    all_listings = []
    offset = 0

    while True:
        url = f"https://www.changiairport.com/bin/changiairport/airport/getdirectorylisting.shop.{terminal}.all.{offset}.{LIMIT}.en-SG.data"
        try:
            res = requests.get(url)
            res.raise_for_status()
            data = res.json()

            listings = data.get("data", [])
            if not listings:
                break  # No more data

            all_listings.extend(listings)
            offset += LIMIT
        except Exception as e:
            print(f"❌ Error fetching page {offset} of {terminal.upper()}: {e}")
            break

    print(f"✅ {len(all_listings)} shopping listings found for {terminal.upper()}")

    # Save to JSON
    os.makedirs("data/structured", exist_ok=True)
    out_path = f"data/structured/{terminal}_shopping.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_listings, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved to {out_path}")

def main():
    for terminal in TERMINALS:
        scrape_terminal_shopping(terminal)

if __name__ == "__main__":
    main()
