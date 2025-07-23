import json
import re
import os

def clean_text(text):
    # Basic cleaning: remove extra spaces, line breaks, weird symbols
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # remove non-ASCII
    return text.strip()

def chunk_text(text, max_tokens=500):
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence.split()) <= max_tokens:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def process_changi_raw():
    input_path = "data/raw/changi_raw.json"
    output_path = "data/cleaned/changi_chunks.json"

    os.makedirs("data/cleaned", exist_ok=True)

    with open(input_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    all_chunks = []
    for url, content in raw_data.items():
        print(f"Processing: {url}")
        cleaned = clean_text(content)
        chunks = chunk_text(cleaned)
        for chunk in chunks:
            all_chunks.append({
                "source": url,
                "content": chunk
            })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"✅ Cleaned and chunked {len(all_chunks)} text blocks → saved to {output_path}")

if __name__ == "__main__":
    process_changi_raw()
