from app.agents.state import RecoveryState
from app.services.llm_service import call_llm

with open("app/agents/prompts/decide_action.txt") as f:
    PROMPT_TEMPLATE = f.read()


def decide_action_node(state: RecoveryState) -> RecoveryState:
    prompt = PROMPT_TEMPLATE.format(
        classified_reason=state["classified_reason"],
        attempt_number=state["attempt_number"],
    )
    result = call_llm(
        system_prompt="You are a precise, rule-following decision engine. Follow the format exactly.",
        user_prompt=prompt,
    )

    # parse the structured response
    action_line = next(l for l in result.splitlines() if l.startswith("ACTION:"))
    reasoning_line = next(l for l in result.splitlines() if l.startswith("REASONING:"))

    state["action"] = action_line.replace("ACTION:", "").strip()
    state["reasoning"] = reasoning_line.replace("REASONING:", "").strip()
    state["should_stop"] = state["action"] in ("escalated", "stopped")

    return state
