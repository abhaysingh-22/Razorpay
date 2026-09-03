# pyrefly: ignore [missing-import]
from langgraph.graph import StateGraph, END
from app.agents.state import RecoveryState
from app.agents.nodes.classify_reason import classify_reason_node
from app.agents.nodes.decide_action import decide_action_node
from app.agents.nodes.execute_retry import execute_retry_node


def build_recovery_graph():
    graph = StateGraph(RecoveryState)

    graph.add_node("classify_reason", classify_reason_node)
    graph.add_node("decide_action", decide_action_node)
    graph.add_node("execute_retry", execute_retry_node)

    graph.set_entry_point("classify_reason")
    graph.add_edge("classify_reason", "decide_action")
    graph.add_edge("decide_action", "execute_retry")
    graph.add_edge("execute_retry", END)

    return graph.compile()


recovery_graph = build_recovery_graph()
