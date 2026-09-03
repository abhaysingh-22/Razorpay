"""
CLI Agent Diagnostic & Node Testing Harness.
Tests individual LangGraph nodes and end-to-end state execution.

Usage:
    python -m scripts.test_agent_node --all
    python -m scripts.test_agent_node --nodes
    python -m scripts.test_agent_node --graph
"""

import argparse
import time
from app.agents.nodes.classify_reason import classify_reason_node
from app.agents.nodes.decide_action import decide_action_node
from app.agents.graph import recovery_graph
from app.services.recovery_service import run_batch_recovery


def get_fresh_state(
    failure_reason: str, attempt_number: int = 1, amount: float = 499.0
) -> dict:
    """Creates a fresh LangGraph state dictionary for testing."""
    return {
        "transaction_id": f"test-tx-{int(time.time())}",
        "amount": amount,
        "failure_reason": failure_reason,
        "customer_id": "cust-test-user-01",
        "attempt_number": attempt_number,
        "classified_reason": None,
        "action": None,
        "reasoning": None,
        "should_stop": False,
        "outcome": None,
        "amount_recovered": 0,
    }


def test_individual_nodes():
    """Tests classify_reason and decide_action nodes across standard failure modes."""
    print("\n" + "=" * 65)
    print("🧪 1. TESTING INDIVIDUAL AGENT NODES (Classify & Decide)")
    print("=" * 65)

    test_scenarios = [
        ("Insufficient Funds (Run 1)", "insufficient_funds", 1, "retry_scheduled"),
        ("Fraud Flag (Immediate Block)", "fraud_flag", 1, "escalated"),
        ("Expired Card (Customer Notice)", "expired_card", 1, "card_update_requested"),
        ("Bank Timeout (Attempt 4 Stopping Rule)", "bank_timeout", 4, "stopped"),
    ]

    for label, reason, attempt, expected_action in test_scenarios:
        state = get_fresh_state(reason, attempt)
        state = classify_reason_node(state)
        state = decide_action_node(state)

        action = state.get("action")
        is_pass = (
            "✅ PASS"
            if action == expected_action
            else f"❌ FAIL (Expected {expected_action})"
        )

        print(f"\nScenario: {label}")
        print(f"  • Input Reason:     {reason} (Attempt #{attempt})")
        print(f"  • Classified Reason: {state.get('classified_reason')}")
        print(f"  • Decided Action:    {action} [{is_pass}]")
        print(f"  • Agent Reasoning:   {state.get('reasoning')}")


def test_graph_execution():
    """Tests the compiled LangGraph StateGraph invocation."""
    print("\n" + "=" * 65)
    print("⚡ 2. TESTING COMPILED LANGGRAPH STATE-MACHINE INVOCATION")
    print("=" * 65)

    graph_scenarios = [
        ("Graph: Insufficient Funds", "insufficient_funds", 1),
        ("Graph: Expired Card", "expired_card", 1),
        ("Graph: Fraud Escalation", "fraud_flag", 1),
        ("Graph: Retry Limit Exhausted", "bank_timeout", 4),
    ]

    for label, reason, attempt in graph_scenarios:
        state = get_fresh_state(reason, attempt)
        result = recovery_graph.invoke(state)

        print(f"\n{label}:")
        print(f"  • Action:   {result.get('action')}")
        print(f"  • Outcome:  {result.get('outcome')}")
        print(f"  • Stop:     {result.get('should_stop')}")


def test_batch_recovery_execution():
    """Runs a full recovery batch against the active database."""
    print("\n" + "=" * 65)
    print("📦 3. TESTING FULL BATCH RECOVERY PIPELINE")
    print("=" * 65)

    res = run_batch_recovery()
    print(f"• Processed Transactions: {res.get('processed')}")
    summary = res.get("summary")
    if summary:
        print(f"• Recovery Rate:          {summary.get('recovery_rate')}%")
        print(
            f"• Total Recovered:        ₹{summary.get('total_amount_recovered', 0):,.2f}"
        )
        print(f"• Key Highlights:         {summary.get('key_highlights')}")


def main():
    parser = argparse.ArgumentParser(
        description="Test and debug LangGraph recovery agent nodes."
    )
    parser.add_argument(
        "--nodes", action="store_true", help="Test individual nodes only"
    )
    parser.add_argument(
        "--graph", action="store_true", help="Test compiled StateGraph only"
    )
    parser.add_argument(
        "--batch", action="store_true", help="Run full batch recovery against database"
    )
    parser.add_argument(
        "--all", "-a", action="store_true", help="Run all node, graph, and batch tests"
    )
    args = parser.parse_args()

    # Default to running nodes & graph if no flag specified
    if not (args.nodes or args.graph or args.batch or args.all):
        test_individual_nodes()
        test_graph_execution()
        return

    if args.nodes or args.all:
        test_individual_nodes()

    if args.graph or args.all:
        test_graph_execution()

    if args.batch or args.all:
        test_batch_recovery_execution()


if __name__ == "__main__":
    main()
