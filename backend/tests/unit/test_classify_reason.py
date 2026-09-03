"""
Unit Tests for Failure Reason Classification Node.
Verifies that gateway error strings are correctly classified into the 4 standard categories:
- insufficient_funds
- expired_card
- bank_timeout
- fraud_flag
"""

# pyrefly: ignore [missing-import]
import pytest
from app.agents.nodes.classify_reason import classify_reason_node


@pytest.mark.parametrize("input_reason,expected_category", [
    ("insufficient_funds", "insufficient_funds"),
    ("Not enough funds in customer account", "insufficient_funds"),
    ("expired_card", "expired_card"),
    ("Card validity expired last month", "expired_card"),
    ("bank_timeout", "bank_timeout"),
    ("Bank gateway connection timed out", "bank_timeout"),
    ("fraud_flag", "fraud_flag"),
    ("Suspicious velocity pattern detected", "fraud_flag"),
])
def test_classify_reason_variations(input_reason, expected_category):
    state = {
        "transaction_id": "test-classify-01",
        "amount": 999.0,
        "failure_reason": input_reason,
        "customer_id": "cust-01",
        "attempt_number": 1,
        "classified_reason": None,
        "action": None,
        "reasoning": None,
        "should_stop": False,
        "outcome": None,
        "amount_recovered": 0,
    }
    result = classify_reason_node(state)
    assert result["classified_reason"] == expected_category
