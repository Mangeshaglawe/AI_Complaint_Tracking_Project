import os

from src.extractors import extract_text


def test_extract_text_txt(tmp_path):
    p = tmp_path / "sample.txt"
    content = "Hello\nCustomer Name: Test User\n"
    p.write_text(content, encoding="utf-8")
    assert "Customer Name: Test User" in extract_text(str(p))
