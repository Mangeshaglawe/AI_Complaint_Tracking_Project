import csv
from pathlib import Path

import src.main as main_mod


class FakeLLMClient:
    def __init__(self, *args, **kwargs):
        pass

    def extract_structured(self, text: str):
        return {
            "customer_name": "Test",
            "email": "test@example.com",
            "phone": "000",
            "complaint_category": "General",
            "issue_description": text[:120],
            "resolution_provided": None,
            "is_complaint": True,
            "escalation_required": False,
            "supporting_document": False,
            "overall_status": "open",
        }

    def generate_email(self, structured: dict):
        return f"Dear {structured.get('customer_name')}, we are working on it."

    def generate_summary(self, structured: dict):
        return "- Overview: ...\n- Recommended: follow up"


def test_run_batch_monkeypatch(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    out_dir = tmp_path / "output"
    data_dir.mkdir()
    # create two sample files
    for i in range(2):
        (data_dir / f"c{i+1}.txt").write_text(f"Complaint {i+1}: problem details", encoding="utf-8")

    monkeypatch.setattr(main_mod, "DATA_DIR", data_dir)
    monkeypatch.setattr(main_mod, "OUT_DIR", out_dir)
    monkeypatch.setattr(main_mod, "LLMClient", FakeLLMClient)

    main_mod.run_batch(max_workers=1)

    report = out_dir / "final_report.csv"
    assert report.exists()
    rows = list(csv.DictReader(report.read_text(encoding="utf-8").splitlines()))
    assert len(rows) == 2
