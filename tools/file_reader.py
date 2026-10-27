import os
from pypdf import PdfReader


def read_file(path: str) -> str:
    """Read a text or PDF file and return its content."""
    if not os.path.exists(path):
        return f"File not found: {path}"

    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text[:3000] if text else "Could not extract text from PDF."

    elif ext in [".txt", ".md", ".py", ".json"]:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return content[:3000]

    else:
        return f"Unsupported file type: {ext}"
