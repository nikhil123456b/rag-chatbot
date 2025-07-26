import os
import json
import glob

OUTPUT_DIR = "data/cleaned"
INPUT_DIR = "data/structured"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def flatten_entry(entry, source_file):
    locations = entry.get("location", [])
    flat_entries = []

    for loc in locations:
        flat = {
            "name": entry.get("title", ""),
            "type": entry.get("type", ""),
            "tags": ", ".join(entry.get("tags", {}).values()),
            "dietary": ", ".join(entry.get("dietaryTags", {}).values()) if entry.get("dietaryTags") else "",
            "cuisine": entry.get("cuisine", ""),
            "area": loc.get("area", ""),
            "unit": loc.get("unit", ""),
            "level": loc.get("level", ""),
            "terminal": loc.get("terminal", ""),
            "timing": loc.get("operatingTime") or f"{loc.get('openingTime', '')} - {loc.get('closingTime', '')}",
            "source_file": os.path.basename(source_file),
        }

        # Create a unified text field
        flat["text"] = (
            f"{flat['name']} ({flat['type']}) - {flat['tags']} {flat['cuisine']} {flat['dietary']}. "
            f"Located at {flat['terminal']} {flat['area']} {flat['level']} {flat['unit']}. "
            f"Timing: {flat['timing']}"
        )

        flat_entries.append(flat)

    return flat_entries

def main():
    all_cleaned = []
    for path in glob.glob(f"{INPUT_DIR}/*.json"):
        with open(path, encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, dict):  # In case of API responses
                    data = data.get("data", [])
                for entry in data:
                    cleaned = flatten_entry(entry, path)
                    all_cleaned.extend(cleaned)
            except Exception as e:
                print(f"❌ Failed to load {path}: {e}")

    print(f"✅ Total cleaned entries: {len(all_cleaned)}")

    with open(f"{OUTPUT_DIR}/cleaned_data.json", "w", encoding="utf-8") as f:
        json.dump(all_cleaned, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
