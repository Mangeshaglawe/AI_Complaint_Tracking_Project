import logging
from pathlib import Path
from typing import Iterator

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx"}


# -------------- Format-specific extractors ----------------

def _extract_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _extract_pdf(path: Path) -> str:
    try:
        import pdfplumber  # type: ignore
    except ImportError as exc:
        raise ImportError(
            "pdfplumber is required for PDF ingestion: pip install pdfplumber"
        ) from exc

    pages: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
    return "\n\n".join(pages)


def _extract_docx(path: Path) -> str:
    try:
        import docx  # type: ignore
    except ImportError as exc:
        raise ImportError(
            "python-docx is required for DOCX ingestion: pip install python-docx"
        ) from exc

    doc = docx.Document(str(path))
    return "\n".join(para.text for para in doc.paragraphs if para.text.strip())


_EXTRACTORS = {
    ".txt": _extract_txt,
    ".pdf": _extract_pdf,
    ".docx": _extract_docx,
}


# ----------------------- Public API --------------------

def _iter_documents(directory: Path) -> Iterator[tuple[Path, str]]:
    for path in sorted(directory.iterdir()):
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            logger.debug("Skipping unsupported file type: %s", path.name)
            continue

        if not path.is_file():
            continue

        extractor = _EXTRACTORS[path.suffix.lower()]
        try:
            text = extractor(path)
            if not text.strip():
                logger.warning("File '%s' produced empty text - skipping.", path.name)
                continue
            logger.info("Ingested '%s' (%d chars)", path.name, len(text))
            yield path, text
        except Exception as exc:
            logger.error("Failed to read '%s': %s", path.name, exc)


def load_documents(directory: Path) -> list[dict]:
    """Return a list of document dicts ready for a processing pipeline."""
    return [
        {"filename": path.name, "path": str(path), "text": text}
        for path, text in _iter_documents(directory)
    ]

