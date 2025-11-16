import os
import spacy
from utils import read_file
import json

# --- Step 1: Load trained model ---
model_path = "models/ioc_ner_model"
nlp = spacy.load(model_path)

# --- Step 2: Function to extract IOCs from text ---
def extract_iocs_from_text(text):
    doc = nlp(text)
    iocs = {}
    for ent in doc.ents:
        iocs.setdefault(ent.label_, []).append(ent.text)
    # Remove duplicates
    for key in iocs:
        iocs[key] = list(set(iocs[key]))
    return iocs

# --- Step 3: Process all files in folder ---
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

# --- Step 4: Output results ---
output_file = "ioc_results.json"
with open(output_file, "w") as f:
    json.dump(all_iocs, f, indent=4)

print(f"IOC extraction completed. Results saved to {output_file}")
