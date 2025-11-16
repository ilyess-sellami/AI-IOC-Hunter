import os
import spacy
import re
from utils import read_file
import json

# --- Step 1: Load trained model ---
model_path = "models/ioc_ner_model"
nlp = spacy.load(model_path, exclude=["lemmatizer"])  # exclude lemmatizer to avoid lookup errors

# --- Step 2: Regex patterns for IOCs ---
regex_patterns = {
    "IP": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "URL": r"https?://[^\s]+|hxxp://[^\s]+",
    "HASH": r"\b[a-fA-F0-9]{32,64}\b"  # MD5/SHA1/SHA256
}

# --- Step 3: Function to extract IOCs ---
def extract_iocs_from_text(text):
    iocs = {}

    # --- AI-based extraction ---
    doc = nlp(text)
    for ent in doc.ents:
        iocs.setdefault(ent.label_, []).append(ent.text)

    # --- Regex-based extraction ---
    for label, pattern in regex_patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            iocs.setdefault(label, []).extend(matches)

    # --- Remove duplicates ---
    for key in iocs:
        iocs[key] = list(set(iocs[key]))

    return iocs

# --- Step 4: Process all files in folder ---
folder_path = "files_to_process/"
all_iocs = {}

for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    try:
        text = read_file(file_path)
        iocs = extract_iocs_from_text(text)
        all_iocs[file_name] = iocs
    except Exception as e:
        print(f"Error processing {file_name}: {e}")

# --- Step 5: Output results ---
output_file = "ioc_results.json"
with open(output_file, "w") as f:
    json.dump(all_iocs, f, indent=4)

print(f"IOC extraction completed. Results saved to {output_file}")
