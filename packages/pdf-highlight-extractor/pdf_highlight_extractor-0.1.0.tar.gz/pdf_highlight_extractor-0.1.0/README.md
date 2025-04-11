# 📘 pdf_highlight_extractor

Extract highlighted text from PDF files using PyMuPDF.

This lightweight utility reads highlights from PDFs, along with the associated page number and highlight color. Perfect for summarizing annotated documents, research papers, or ebooks.

---

## 🔧 Installation

Install from PyPI:

```bash
pip install pdf-highlight-extractor
```

---

## 🚀 Usage

```python
from pdf_highlight_extractor.reader import extract_highlights

highlights = extract_highlights("sample.pdf")

for h in highlights:
    print(f"Page {h['page']} | Color: {h['color']} | Text: {h['text']}")
```

### 📝 Output Example

```text
Page 2 | Color: (1.0, 1.0, 0.0) | Text: This is a highlighted phrase
Page 5 | Color: (0.0, 1.0, 0.0) | Text: Another important note
```

---

## 🧠 Features

- ✅ Extract text from highlights
- ✅ Get page number and highlight color
- ✅ Fallback extraction if highlight text is not directly stored
- ✅ Simple API for automation or personal use

---

## 🧪 Example PDF

You can test the tool using any PDF with highlights created in:
- Adobe Acrobat Reader
- Preview (macOS)
- Xodo or other PDF apps

---

## 📦 Requirements

- Python 3.7+
- PyMuPDF (automatically installed)

> Only needed for development:

```bash
pip install -e .
```

---

## 📄 License

MIT License © 2025 Anish Bala Sachin
```

Let me know if you'd like to add:
- A "Contributing" section
- Badges (PyPI version, license, etc.)
- GitHub Actions badge for testing