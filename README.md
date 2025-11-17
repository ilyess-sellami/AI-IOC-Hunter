# 🔥 AI IOC Hunter

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