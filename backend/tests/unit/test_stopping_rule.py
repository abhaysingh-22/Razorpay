from app.agents.nodes.decide_action import decide_action_node

def test_stops_after_max_attempts():
    state = {"classified_reason": "bank_timeout", "attempt_number": 4, "action": None, "reasoning": None, "should_stop": False}
    result = decide_action_node(state)
    assert result["action"] == "stopped"

def test_fraud_always_escalates():
    state = {"classified_reason": "fraud_flag", "attempt_number": 1, "action": None, "reasoning": None, "should_stop": False}
    result = decide_action_node(state)
    assert result["action"] == "escalated"