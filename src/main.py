import os
import json
import csv
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .extractors import extract_text
from .llm_client import LLMClient
from .models import ComplaintData


logging.basicConfig(level=logging.INFO)


BASE = Path(__file__).resolve().parent.parent
DATA_DIR = BASE / "data"
OUT_DIR = BASE / "output"


def ensure_dirs():
    (OUT_DIR / "structured_data").mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "customer_emails").mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "case_summaries").mkdir(parents=True, exist_ok=True)


def process_file(path: Path, client: LLMClient):
    logging.info(f"Processing {path.name}")
    try:
        text = extract_text(str(path))
    except Exception as e:
        logging.exception("Extraction failed")
        return {"filename": path.name, "error": str(e)}

    try:
        structured = client.extract_structured(text)
    except Exception as e:
        logging.exception("Structured extraction failed")
        return {"filename": path.name, "error": str(e), "raw_text": text[:200]}

    # validate with Pydantic
    try:
        # coerce None values for boolean fields to False so Pydantic accepts them
        for _b in ("is_complaint", "escalation_required", "supporting_document"):
            if structured.get(_b) is None:
                structured[_b] = False

        data = ComplaintData(**structured)
    except Exception as e:
        logging.exception("Validation failed")
        return {"filename": path.name, "error": f"validation: {e}", "structured": structured}

    # generate email and summary
    email = client.generate_email(structured)
    summary = client.generate_summary(structured)

    base = OUT_DIR / "structured_data" / (path.stem + ".json")
    with open(base, "w", encoding="utf-8") as f:
        json.dump(structured, f, indent=2, default=str)

    email_path = OUT_DIR / "customer_emails" / (path.stem + ".txt")
    with open(email_path, "w", encoding="utf-8") as f:
        f.write(email)

    summary_path = OUT_DIR / "case_summaries" / (path.stem + ".txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)

    def safe_rel(path_value: Path) -> str:
        try:
            return str(path_value.relative_to(BASE))
        except ValueError:
            return str(path_value)

    return {
        "filename": path.name,
        "customer_name": data.customer_name,
        "email": str(data.email) if data.email else None,
        "phone": data.phone,
        "category": data.complaint_category,
        "escalation_required": data.escalation_required,
        "overall_status": data.overall_status,
        "structured_path": safe_rel(base),
        "email_path": safe_rel(email_path),
        "summary_path": safe_rel(summary_path),
    }


def run_batch(max_workers: int = 4, progress_callback=None, state=None):
    ensure_dirs()
    files = [p for p in DATA_DIR.iterdir() if p.is_file()]
    if state is not None:
        state["files"] = [p.name for p in files]
        state["total_documents"] = len(files)
        state["processed_documents"] = 0
        state["status"] = "running"
        state["results"] = []
        state["errors"] = []

    if progress_callback is not None:
        progress_callback({
            "type": "start",
            "total": len(files),
            "status": "running",
        })

    try:
        client = LLMClient()
    except Exception as exc:
        if state is not None:
            state["status"] = "error"
            state["errors"].append(str(exc))
        if progress_callback is not None:
            progress_callback({"type": "error", "message": str(exc), "status": "error"})
        raise

    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(process_file, p, client): p for p in files}
        for idx, fut in enumerate(as_completed(futures), start=1):
            res = fut.result()
            results.append(res)
            if state is not None:
                state["results"].append(res)
                state["processed_documents"] = idx
                if res.get("error"):
                    state["errors"].append({"filename": res.get("filename"), "error": res.get("error")})
            if progress_callback is not None:
                progress_callback({
                    "type": "progress",
                    "processed": idx,
                    "total": len(files),
                    "filename": res.get("filename"),
                    "error": res.get("error"),
                    "status": "running",
                })

    report_path = OUT_DIR / "final_report.csv"
    keys = [
        "filename",
        "customer_name",
        "email",
        "phone",
        "category",
        "escalation_required",
        "overall_status",
        "structured_path",
        "email_path",
        "summary_path",
        "error",
    ]
    with open(report_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in results:
            writer.writerow({k: r.get(k, None) for k in keys})

    if state is not None:
        state["status"] = "completed"
        state["report_path"] = str(report_path)
        state["success_count"] = sum(1 for r in results if not r.get("error"))
        state["error_count"] = sum(1 for r in results if r.get("error"))

    if progress_callback is not None:
        progress_callback({
            "type": "complete",
            "total": len(files),
            "status": "completed",
            "success_count": sum(1 for r in results if not r.get("error")),
            "error_count": sum(1 for r in results if r.get("error")),
        })

    logging.info(f"Batch finished. Report: {report_path}")
    return results


if __name__ == "__main__":
    run_batch()
