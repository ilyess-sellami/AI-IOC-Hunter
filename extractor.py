import spacy
import re

# ------------------------------------------------------
# 1. Load trained AI model
# ------------------------------------------------------
model_path = "models/ioc_ner_model"
nlp = spacy.load(model_path, exclude=["lemmatizer"])  # avoid lookup-table errors


# ------------------------------------------------------
# 2. Strong regex patterns
# ------------------------------------------------------
regex_patterns = {
    # Valid IPv4 format (does NOT fully validate 0–255, but cleaner)
    "IP": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",

    # Email
    "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",

    # URL (http + hxxp + https)
    "URL": r"(?:https?|hxxp)://[^\s]+",

    # Hashes (MD5, SHA1, SHA256)
    "HASH": r"\b[a-fA-F0-9]{32,64}\b",

    # Domain (NO http, NO emails, NO IPs)
    "DOMAIN": r"\b(?!(?:\d{1,3}\.){3}\d{1,3})(?![A-Za-z0-9._%+-]+@)[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
}


# ------------------------------------------------------
# 3. Extractor function (AI + regex + cleanup)
# ------------------------------------------------------
def extract_iocs_from_text(text):
    iocs = {}

    # ---------- AI extraction ----------
    doc = nlp(text)
    for ent in doc.ents:
        iocs.setdefault(ent.label_, []).append(ent.text)

    # ---------- Regex extraction ----------
    for label, pattern in regex_patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            iocs.setdefault(label, []).extend(matches)

    # ---------- Cleanup results ----------
    cleaned_iocs = {}

    for key, values in iocs.items():
        unique_vals = set(v.strip() for v in values)

        # Cleanup for each IOC type
        if key == "IP":
            cleaned_iocs[key] = [
                v for v in unique_vals
                if re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", v)
                and not any(len(p) > 3 for p in v.split("."))  # avoid crazy numbers
            ]

        elif key == "DOMAIN":
            cleaned_iocs[key] = [
                v for v in unique_vals
                if v not in iocs.get("EMAIL", [])
                and not re.match(r"(?:\d{1,3}\.){3}\d{1,3}", v)
                and not v.startswith("http")
            ]

        elif key == "HASH":
            cleaned_iocs[key] = [
                v for v in unique_vals if len(v) in (32, 40, 64)
            ]

        else:
            cleaned_iocs[key] = list(unique_vals)

    return cleaned_iocs
