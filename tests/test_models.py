from src.models import ComplaintData


def test_complaint_model_basic():
    d = {
        "customer_name": "Alice",
        "email": "alice@example.com",
        "is_complaint": True,
        "escalation_required": False,
    }
    obj = ComplaintData(**d)
    assert obj.customer_name == "Alice"
    assert obj.email == "alice@example.com"
