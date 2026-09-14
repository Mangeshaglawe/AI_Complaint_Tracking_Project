import os
from typing import Optional


def extract_text(file_path: str) -> str:
    """Extract text from txt, pdf, docx files."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    if ext == ".pdf":
        try:
            from PyPDF2 import PdfReader

            reader = PdfReader(file_path)
            parts = []
            for p in reader.pages:
                t = p.extract_text()
                if t:
                    parts.append(t)
            return "\n".join(parts)
        except Exception as e:
            raise RuntimeError(f"PDF extraction failed: {e}")

    if ext == ".docx":
        try:
            from docx import Document

            doc = Document(file_path)
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception as e:
            raise RuntimeError(f"DOCX extraction failed: {e}")

    raise ValueError(f"Unsupported file type: {ext}")
