from app.agents.nodes.classify_reason import classify_reason_node
from app.agents.nodes.decide_action import decide_action_node
from app.agents.nodes.execute_retry import execute_retry_node
from app.agents.graph import recovery_graph
from app.services.recovery_service import run_batch_recovery

def fresh_state(failure_reason, attempt_number=1):
    return {
        "transaction_id": "test-1",
        "amount": 499,
        "failure_reason": failure_reason,
        "customer_id": "cust-1",
        "attempt_number": attempt_number,
        "classified_reason": None,
        "action": None,
        "reasoning": None,
        "should_stop": False,
        "outcome": None,
        "amount_recovered": 0,
    }

def run_case(label, failure_reason, attempt_number=1):
    print(f"\n--- {label} ---")
    state = fresh_state(failure_reason, attempt_number)
    state = classify_reason_node(state)
    state = decide_action_node(state)
    print("classified_reason:", state["classified_reason"])
    print("action:", state["action"])
    print("reasoning:", state["reasoning"])
    print("should_stop:", state["should_stop"])
    return state

# if __name__ == "__main__":
#     run_case("Insufficient funds, attempt 1", "insufficient_funds", attempt_number=1)
#     run_case("Fraud flag, attempt 1", "fraud_flag", attempt_number=1)
#     run_case("Expired card, attempt 1", "expired_card", attempt_number=1)
#     run_case("Bank timeout, attempt 4 (should stop)", "bank_timeout", attempt_number=4)

def run_full_case(label, failure_reason, attempt_number=1):
    state = fresh_state(failure_reason, attempt_number)
    state = classify_reason_node(state)
    state = decide_action_node(state)
    state = execute_retry_node(state)
    print(f"\n--- {label} ---")
    print("action:", state["action"], "| outcome:", state["outcome"])

def run_graph_case(label, failure_reason, attempt_number=1):
    state = fresh_state(failure_reason, attempt_number)
    result = recovery_graph.invoke(state)
    print(f"\n--- GRAPH: {label} ---")
    print("action:", result["action"], "| outcome:", result["outcome"])
    

if __name__ == "__main__":
    run_case("Insufficient funds, attempt 1", "insufficient_funds", attempt_number=1)
    run_case("Fraud flag, attempt 1", "fraud_flag", attempt_number=1)
    run_case("Expired card, attempt 1", "expired_card", attempt_number=1)
    run_case("Bank timeout, attempt 4 (should stop)", "bank_timeout", attempt_number=4)

    run_full_case("Full flow — insufficient funds", "insufficient_funds")
    run_full_case("Full flow — expired card", "expired_card")
    run_full_case("Full flow — fraud flag", "fraud_flag")
    run_full_case("Full flow — stopped case", "bank_timeout", attempt_number=4)
    
    run_graph_case("Graph — insufficient funds", "insufficient_funds")
    run_graph_case("Graph — expired card", "expired_card")
    run_graph_case("Graph — fraud flag", "fraud_flag")
    run_graph_case("Graph — stopped case", "bank_timeout", attempt_number=4)
    
    print("\n--- RUNNING FULL BATCH ---")
    batch_result = run_batch_recovery()
    print("Processed:", batch_result["processed"])
    print("Summary:", batch_result["summary"])