# AI IOC Hunter - AI-Powered IOC Extractor

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Build](https://img.shields.io/badge/Build-Passing-brightgreen)](#)
[![Issues](https://img.shields.io/badge/Issues-0-orange)](#)
[![GitHub Repo](https://img.shields.io/badge/GitHub-AI--IOC--Hunter-black?logo=github)](https://github.com/ilyess-sellami/AI-IOC-Hunter)

![AI IOC Hunter](/images/Banner-Image.png)

**AI IOC Hunter** is a Python-based command-line tool for extracting **[Indicators of Compromise (IOCs)](https://www.fortinet.com/resources/cyberglossary/indicators-of-compromise)** such as IPs, domains, URLs, hashes, and emails from files or directories. The tool combines **[AI-powered NER (spaCy)](https://spacy.io/)** and **[regex patterns](https://en.wikipedia.org/wiki/Regular_expression)** to provide accurate IOC detection.  

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

![AI Model (spaCy NER + Custom Fine‑Tuning)](/images/SpaCy-NER.png)

The core of the tool is a **custom spaCy Named Entity Recognition (NER) model** trained specifically to detect cybersecurity IOCs.

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

**💡 Key Points:**

- **text**: Contains the raw log or text snippet.
- **entities**: List of `[start, end, label]` triples, where `start` and `end` are character offsets and `label` is the entity type (e.g., `IP`, `DOMAIN`, `URL`, `EMAIL`, `HASH`).
- **Expandable Dataset**: Add more JSON files to `/data/` (e.g., `train_data_24.json`, `train_data_25.json`) to improve model performance. The training script automatically loads **all JSON files**, so the model evolves as the dataset grows.
- **Adaptive Learning**: This structure allows AI IOC Hunter to learn from real-world threat examples, improving detection accuracy and adapting to new types of IOCs.

### 🧪 3. Hybrid Detection (AI + Regex Rules)

IOC Hunter uses a **dual‑layer detection pipeline**:

1. **AI Layer (NER Model)**

    - Understands context
    - Detects IOCs even when obfuscated or written in unusual formats
    - Survives noisy text (PDF extra whitespace, malformed logs, etc.)

2. **Regex Layer (Rule-Based Engine)**

    - Ensures no classic IOC format is missed
    - Validates/corrects AI‑detected patterns
    - Adds coverage for edge cases

```sql
AI → Regex Validation → Final IOC List
```

The combination gives **high recall + high precision**.


### 📂 4. Multi‑Format File Analysis

The CLI automatically extracts readable text from:

| File Type                                                   | Method                                    |
| ----------------------------------------------------------- | ----------------------------------------- |
| `.pdf`                                                      | PyPDF2 text extraction                    |
| `.docx`                                                     | python-docx                               |
| `.txt`, `.log`, `.cfg`, `.ini`                              | direct read                               |
| `.py`, `.js`, `.php`, `.cpp`, `.json`, `.yml`, `.xml`, etc. | code‑safe text parsing                    |
| `.exe`, `.bin`, `.dat`, etc.                                | Binary files decoded with `chardet`.      |

You can point the tool at any file:

```bash
python main.py incident_report.pdf
```

### 📑 5. Smart Output Export

Export results in **JSON**, **CSV**, or **TXT**:

```bash
python main.py /path/to/files -o results.csv -f csv
```

---

## 💾 Training the Model

If you want to **retrain or improve the model**:

```bash
python train_model.py
```

- Training data is stored in `data/*.json`
- Labels: `IP`, `DOMAIN`, `URL`, `HASH`, `EMAIL`
- Uses **spaCy NER** and supports adding more JSON training files

Make sure your training examples are clean and properly aligned to avoid errors.

---

## 🏁 Conclusion

**AI IOC Hunter** is a **powerful**, **extensible**, and **adaptive** tool for cybersecurity analysts and SOC teams. With **AI-driven NER**, **regex validation**, and support for multiple file types, it simplifies the process of detecting and extracting Indicators of Compromise.

It is **fully expandable**, allowing you to continuously improve detection by adding new training data, and integrates seamlessly into automated pipelines or manual analysis workflows.
