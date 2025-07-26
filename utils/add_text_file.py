# utils/add_text_field.py

import json
import os

INPUT_PATH = "data/cleaned/cleaned_data.json"
OUTPUT_PATH = "data/cleaned/cleaned_data_with_text.json"

# Helper function to generate a readable 'text' field
def generate_text(entry):
    name = entry.get("name", "")
    type_ = entry.get("type", "")
    location = entry.get("location", "")
    timing = entry.get("timing", "")
    features = ", ".join(entry.get("features", [])) if "features" in entry else ""
    description = f"{name} ({type_}) located at {location}."
    if features:
        description += f" Features include {features}."
    if timing:
        description += f" Open {timing}."
    return description

# Load original records
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    records = json.load(f)

# Add 'text' field if missing
updated_records = []
for entry in records:
    if "text" not in entry:
        entry["text"] = generate_text(entry)
    updated_records.append(entry)

# Save updated records
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(updated_records, f, ensure_ascii=False, indent=2)

print(f"✅ Updated records saved to {OUTPUT_PATH} with {len(updated_records)} entries.")
