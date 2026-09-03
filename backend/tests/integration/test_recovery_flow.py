"""
Integration Tests for Razorpay RecoverAI APIs and Recovery Flow.
Tests end-to-end FastAPI routes, database interactions, and business pipelines.
"""

# pyrefly: ignore [missing-import]
import pytest


def test_health_check(client):
    """Verifies that the core API server starts and responds healthy."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json().get("status") == "ok"


def test_generate_transactions_endpoint(client):
    """Verifies that synthetic failed payments can be injected."""
    response = client.post("/api/v1/transactions/generate?count=5")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["inserted"] == 5
    assert len(data["transactions"]) == 5
    assert "amount" in data["transactions"][0]
    assert "failure_reason" in data["transactions"][0]


def test_recovery_batch_execution(client):
    """Verifies that batch recovery executes and returns a valid summary."""
    # Ensure there is at least some data
    client.post("/api/v1/transactions/generate?count=3")

    response = client.post("/api/v1/recovery/run")
    assert response.status_code == 200
    data = response.json()
    assert "processed" in data
    assert "summary" in data
    assert "recovery_rate" in data["summary"]
    assert "roi_metrics" in data["summary"]


def test_metrics_summary_endpoint(client):
    """Verifies that the summary headline and ROI metrics are returned correctly."""
    response = client.get("/api/v1/metrics/summary")
    assert response.status_code == 200
    data = response.json()
    if data is not None:
        assert "total_transactions" in data
        assert "total_amount_at_risk" in data
        assert "recovery_rate" in data
        assert "roi_metrics" in data
        assert "recovered_arr" in data["roi_metrics"]
        assert "benchmark_uplift" in data["roi_metrics"]


def test_export_pdf_report_endpoint(client):
    """Verifies that the PDF export endpoint returns valid application/pdf binary content."""
    response = client.get("/api/v1/metrics/export-pdf")
    assert response.status_code == 200
    assert "application/pdf" in response.headers.get("content-type", "")
    assert len(response.content) > 1000  # Non-empty PDF binary
    assert response.content.startswith(b"%PDF")


def test_human_review_queue_and_resolution(client):
    """Verifies the Human-in-the-Loop review queue and manual approval flow."""
    # 1. Fetch current review queue
    queue_res = client.get("/api/v1/recovery/review-queue")
    assert queue_res.status_code == 200
    queue = queue_res.json()
    assert isinstance(queue, list)

    # 2. If an item exists in the queue, test resolution
    if queue:
        target_tx = queue[0]
        tx_id = target_tx["id"]

        resolve_res = client.post(
            f"/api/v1/recovery/review-queue/{tx_id}/resolve",
            json={
                "decision": "approve",
                "notes": "Automated integration test approval",
            },
        )
        assert resolve_res.status_code == 200
        result = resolve_res.json()
        assert result["status"] == "success"
        assert result["new_status"] == "recovered"
