import spacy
from spacy.training.example import Example
from spacy.util import minibatch
import json
import random
import pandas as pd
import os
import glob

# --- Step 1: Load all training data from JSON files ---
TRAIN_DATA = []

data_files = glob.glob("data/*.json")
for file in data_files:
    with open(file, "r") as f:
        raw_data = json.load(f)
        for item in raw_data:
            # Convert entities to tuple and filter invalid ones
            entities = [tuple(ent) for ent in item.get("entities", []) if len(ent) == 3]
            TRAIN_DATA.append((item["text"], {"entities": entities}))

print(f"Loaded {len(TRAIN_DATA)} training examples from {len(data_files)} files")

# Optional: inspect some data
df = pd.DataFrame({"text": [t[0] for t in TRAIN_DATA]})
print(df.head())

# --- Step 2: Load pretrained English model ---
nlp = spacy.load("en_core_web_sm") 

# Add NER pipeline if not present
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner")
else:
    ner = nlp.get_pipe("ner")

# Add your labels
labels = ["IP", "DOMAIN", "URL", "HASH", "EMAIL"]
for label in labels:
    ner.add_label(label)

# --- Step 3: Helper function to remove overlapping entities ---
def remove_overlaps(entities):
    """
    Remove or skip overlapping entities to avoid SpaCy crash.
    """
    # Sort by start index
    entities = sorted(entities, key=lambda x: (x[0], x[1]))
    cleaned = []
    for start, end, label in entities:
        overlap = False
        for c_start, c_end, c_label in cleaned:
            if start < c_end and end > c_start:
                overlap = True
                break
        if not overlap:
            cleaned.append((start, end, label))
    return cleaned

# --- Step 4: Training ---
optimizer = nlp.begin_training()
n_iter = 20  # adjust as needed

for epoch in range(n_iter):
    random.shuffle(TRAIN_DATA)
    losses = {}
    batches = minibatch(TRAIN_DATA, size=2)
    
    for batch in batches:
        examples = []
        for text, ann in batch:
            doc = nlp.make_doc(text)
            
            # Remove duplicates & overlapping entities
            ann["entities"] = remove_overlaps(list(set(ann.get("entities", []))))
            
            if not ann["entities"]:
                continue

            examples.append(Example.from_dict(doc, ann))

        if examples:
            nlp.update(
                examples,
                sgd=optimizer,
                drop=0.2,
                losses=losses
            )

    print(f"Epoch {epoch+1}/{n_iter}, Losses: {losses}")

# --- Step 5: Save the trained model ---
model_path = "models/ioc_ner_model"
os.makedirs(model_path, exist_ok=True)
nlp.to_disk(model_path)
print(f"Model saved to {model_path}")

# --- Step 6: Test the trained model ---
test_text = (
    "Suspicious IP 192.168.1.100 contacted evil.com and downloaded hash "
    "e99a18c428cb38d5f260853678922e03, attacker email: fraudster@example.com"
)
doc = nlp(test_text)
print("\nExtracted IOCs:")
for ent in doc.ents:
    print(ent.text, ":", ent.label_)
