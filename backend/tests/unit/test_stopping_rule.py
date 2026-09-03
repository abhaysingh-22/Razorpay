"""
Unit Tests for Agent Stopping & Action Decision Policies.
Verifies that the LLM/Rule engine follows business safety rules.
"""

# pyrefly: ignore [missing-import]
import pytest
from app.agents.nodes.decide_action import decide_action_node


def test_stops_after_max_attempts():
    """Attempt 4+ must strictly halt further retries (stopping rule)."""
    state = {
        "classified_reason": "bank_timeout",
        "attempt_number": 4,
        "action": None,
        "reasoning": None,
        "should_stop": False,
    }
    result = decide_action_node(state)
    assert result["action"] == "stopped"
    assert result["should_stop"] is True


def test_fraud_always_escalates():
    """Fraud flags must immediately escalate with zero auto-retries."""
    state = {
        "classified_reason": "fraud_flag",
        "attempt_number": 1,
        "action": None,
        "reasoning": None,
        "should_stop": False,
    }
    result = decide_action_node(state)
    assert result["action"] == "escalated"
    assert result["should_stop"] is True


def test_insufficient_funds_schedules_retry():
    """Attempt 1 for insufficient funds must schedule a delayed retry."""
    state = {
        "classified_reason": "insufficient_funds",
        "attempt_number": 1,
        "action": None,
        "reasoning": None,
        "should_stop": False,
    }
    result = decide_action_node(state)
    assert result["action"] == "retry_scheduled"
    assert result["should_stop"] is False


def test_expired_card_requests_update():
    """Expired cards should ask customer to update card rather than retrying directly."""
    state = {
        "classified_reason": "expired_card",
        "attempt_number": 1,
        "action": None,
        "reasoning": None,
        "should_stop": False,
    }
    result = decide_action_node(state)
    assert result["action"] == "card_update_requested"
    assert result["should_stop"] is False