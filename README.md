# AI IOC Hunter

![AI IOC Hunter](/images/Banner-Image.png)

**AI IOC Hunter** is a Python-based command-line tool for extracting **Indicators of Compromise (IOCs)** such as IPs, domains, URLs, hashes, and emails from files or directories. The tool combines **AI-powered NER (spaCy)** and **regex patterns** to provide accurate IOC detection.  

---

## ⚡ Features
- Extracts IOCs: **IP**, **DOMAIN**, **URL**, **HASH**, **EMAIL**
- Supports multiple file types: `.txt`, `.pdf`, `.docx`, `.log`, `.py`, `.cpp`, `.php`, `.exe`, and more
- Recursively scan directories
- Live monitoring mode (`tail -f`) for log files
- Save results in multiple formats: **JSON**, **CSV**, **TXT**
- ASCII banner for a clean, Metasploit-like CLI interface
- Clean and fast CLI interface powered by **Typer** and **Rich**

---

## 🛠 Installation

### 1. Clone the repository

```bash
git clone https://github.com/ilyess-sellami/AI-IOC-Hunter.git
cd AI-IOC-Hunter
```

### 2. Create virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Make sure you have the trained model in `models/ioc_ner_model`. You can train it using `train_model.py` if needed.

---

## 🚀 Usage

### Scan a single file

```bash
python main.py /path/to/file.txt
```

### Scan a folder recursively

```bash
python main.py /path/to/folder --recursive
```

### Tail a log file in real-time

```bash
python main.py /path/to/logfile.log --tail
```

### Specify output file and format

```bash
python main.py /path/to/files -o results.json -f json
python main.py /path/to/files -o results.csv -f csv
python main.py /path/to/files -o results.txt -f txt
```

---

## 🧠 How It Works — Inside the AI Engine

**AI IOC Hunter** combines **AI‑powered Entity Recognition**, **pattern‑based detection**, and **multi‑format document parsing** to extract Indicators of Compromise (IOCs) with high accuracy.

### 🔍 1. AI Model (spaCy NER + Custom Fine‑Tuning)

The core of the tool is a **custom [spaCy Named Entity Recognition (NER) model](https://spacy.io/universe/project/video-spacys-ner-model)** trained specifically to detect cybersecurity IOCs.

The model identifies entities such as:

- **IP addresses**
- **Domains**
- **URLs**
- **Email addresses**
- **File hashes** (MD5, SHA1, SHA256)

### 📚 2. Training Dataset

The AI IOC Hunter model is trained on a **rich and growing dataset** located in the `/data/` folder. This dataset contains **multiple JSON files** with realistic threat intelligence examples, covering a wide variety of IOCs:

```bash
/data/
    train_data_1.json
    train_data_2.json
    train_data_3.json
    ...
    train_data_23.json
```

Each JSON file in the `/data/` folder contains **labeled examples** with text and annotated entities that the model uses for training. Entities include **IP addresses, domains, URLs, emails, hashes**, and other indicators of compromise (IOCs).

Example of a JSON training file:

```json
[
  {
    "text": "IP 198.51.100.10 attempted brute force attack on admin portal admin.internal.net",
    "entities": [[3, 15, "IP"], [52, 72, "DOMAIN"]]
  },
  {
    "text": "Email phishing alert from user@weird-domain.biz with attachment hash d41d8cd98f00b204e9800998ecf8427e",
    "entities": [[28, 50, "EMAIL"], [70, 102, "HASH"]]
  },
  {
    "text": "Malware downloaded via URL http://dangerous-site.com/path/to/file.exe on victim machine",
    "entities": [[29, 74, "URL"]]
  }
]
```

💡 Expandable: You can always add more training files to `/data/` (e.g., `train_data_24.json`, `train_data_25.jso`n) to improve model performance. The training script automatically loads **all JSON files** in the folder, so your model evolves as your dataset grows.

This ensures that AI IOC Hunter **learns from real-world threat examples**, improves detection accuracy, and adapts to new types of IOCs.