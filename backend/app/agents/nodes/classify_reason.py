from app.agents.state import RecoveryState
from app.services.llm_service import call_llm

with open("app/agents/prompts/classify_reason.txt") as f:
    PROMPT_TEMPLATE = f.read()

def classify_reason_node(state: RecoveryState) -> RecoveryState:
    prompt = PROMPT_TEMPLATE.format(failure_reason=state["failure_reason"])
    result = call_llm(
        system_prompt="You are a precise classifier. Respond with only the category name.",
        user_prompt=prompt,
    )
    state["classified_reason"] = result.strip().lower()
    return state
