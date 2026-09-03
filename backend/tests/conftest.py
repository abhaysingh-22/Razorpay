# pyrefly: ignore [missing-import]
import pytest
# pyrefly: ignore [missing-import]
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="session")
def client():
    """Shared FastAPI test client for integration tests."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def sample_transaction_state():
    """Generates a standard test state dictionary for agent node tests."""
    return {
        "transaction_id": "test-tx-001",
        "amount": 1499.00,
        "failure_reason": "insufficient_funds",
        "customer_id": "cust-test-001",
        "attempt_number": 1,
        "classified_reason": None,
        "action": None,
        "reasoning": None,
        "should_stop": False,
        "outcome": None,
        "amount_recovered": 0,
    }
