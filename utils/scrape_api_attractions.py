import requests
import json
import os

TERMINALS = ["t1", "t2", "t3", "t4", "j1"]
LIMIT = 15

def scrape_attractions(terminal):
    print(f"\n🎡 Scraping Attractions – {terminal.upper()}")
    all_attractions = []
    offset = 0

    while True:
        url = f"https://www.changiairport.com/bin/changiairport/airport/getattractionslistingcards.{terminal}.all.all.{offset}.{LIMIT}.en-SG.data"
        try:
            res = requests.get(url)
            res.raise_for_status()
            data = res.json()

            listings = data.get("data", [])
            if not listings:
                break

            all_attractions.extend(listings)
            offset += LIMIT
        except Exception as e:
            print(f"❌ Error on {terminal.upper()} page {offset}: {e}")
            break

    print(f"✅ {len(all_attractions)} attractions found for {terminal.upper()}")

    os.makedirs("data/structured", exist_ok=True)
    out_path = f"data/structured/{terminal}_attractions.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_attractions, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved to {out_path}")

def main():
    for terminal in TERMINALS:
        scrape_attractions(terminal)

if __name__ == "__main__":
    main()
