import PyPDF2
from docx import Document
import os
import chardet

# --- PDF Reader ---
def read_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"[WARN] Could not read PDF {file_path}: {e}")
    return text

# --- DOCX Reader ---
def read_docx(file_path):
    text = ""
    try:
        doc = Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        print(f"[WARN] Could not read DOCX {file_path}: {e}")
    return text

# --- Plain text or code reader ---
def read_text_file(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'
            text = raw_data.decode(encoding, errors='ignore')
    except Exception as e:
        print(f"[WARN] Could not read text/code file {file_path}: {e}")
    return text

# --- Generic file reader ---
def read_file(file_path):
    if not os.path.isfile(file_path):
        raise ValueError(f"File does not exist: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.pdf':
        return read_pdf(file_path)
    elif ext == '.docx':
        return read_docx(file_path)
    elif ext in ['.txt', '.log', '.py', '.cpp', '.c', '.php', '.js', '.java', '.rb', '.go', '.ts', '.html', '.css']:
        return read_text_file(file_path)
    else:
        print(f"[WARN] Unsupported file type {ext}, reading as text fallback")
        return read_text_file(file_path)
