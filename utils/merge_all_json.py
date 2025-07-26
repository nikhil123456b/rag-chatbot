# utils/merge_all_json.py

import json
import os

# All file names in raw directory
json_files = [
    "lounges.json",
    "attractions.json",
    "medical_wellness.json",
    "baggage_services.json",
    "hotel_showers.json",
    "wifi_charging_prayer.json"
]

merged_data = []

# Load and combine each file
for filename in json_files:
    path = os.path.join("data", "raw", filename)
    with open(path, "r", encoding="utf-8") as f:
        merged_data.extend(json.load(f))

# Save to cleaned_data.json
os.makedirs("data/cleaned", exist_ok=True)
with open("data/cleaned/cleaned_data.json", "w", encoding="utf-8") as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=2)

print(f"✅ Merged {len(json_files)} files with total {len(merged_data)} entries.")
