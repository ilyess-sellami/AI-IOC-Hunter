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

data_files = glob.glob("data/*.json")  # automatically find all json files in data/
for file in data_files:
    with open(file, "r") as f:
        raw_data = json.load(f)
        for item in raw_data:
            TRAIN_DATA.append((item["text"], {"entities": [tuple(ent) for ent in item["entities"]]}))

print(f"Loaded {len(TRAIN_DATA)} training examples from {len(data_files)} files")

# Optional: inspect some data
df = pd.DataFrame({"text": [t[0] for t in TRAIN_DATA]})
print(df.head())

# --- Step 2: # Load pretrained English model ---
nlp = spacy.load("en_core_web_sm")

# Add NER pipeline
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner")
else:
    ner = nlp.get_pipe("ner")

# Add labels
labels = ["IP", "DOMAIN", "URL", "HASH", "EMAIL"]
for label in labels:
    ner.add_label(label)

# --- Step 3: Training ---
optimizer = nlp.begin_training()

n_iter = 20  # adjust if needed
for epoch in range(n_iter):
    random.shuffle(TRAIN_DATA)
    losses = {}
    batches = minibatch(TRAIN_DATA, size=2)
    for batch in batches:
        for text, annotations in batch:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], sgd=optimizer, drop=0.2, losses=losses)
    print(f"Epoch {epoch+1}/{n_iter}, Losses: {losses}")

# --- Step 4: Save trained model ---
model_path = "models/ioc_ner_model"
os.makedirs(model_path, exist_ok=True)
nlp.to_disk(model_path)
print(f"Model saved to {model_path}")

# --- Step 5: Test trained model ---
test_text = "Suspicious IP 192.168.1.100 contacted evil.com and downloaded hash e99a18c428cb38d5f260853678922e03"
doc = nlp(test_text)
print("\nExtracted IOCs:")
for ent in doc.ents:
    print(ent.text, ":", ent.label_)
