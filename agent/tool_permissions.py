# agent/tool_permissions.py
from fastapi import HTTPException

ROLE_TOOL_PERMISSIONS = {
    "user": {
        "intent_classifier",
        "planner",
        "generate_answer",
        "retrieve_context",
        "get_tasks",
        "prioritize_tasks",  # 🧠 NEW
    },
    "admin": {
        "intent_classifier",
        "planner",
        "generate_answer",
        "retrieve_context",
        "get_tasks",
        "create_task",
        "prioritize_tasks",  # 🧠 NEW
    },
}

def is_tool_allowed(user, tool_name: str) -> None:
    if not hasattr(user, "role"):
         raise HTTPException(status_code=403, detail="Role missing")
    role = user.role

    allowed_tools = ROLE_TOOL_PERMISSIONS.get(role, set())

    if tool_name not in allowed_tools:
        raise HTTPException(
            status_code=403,
            detail=f"Tool '{tool_name}' not allowed for role '{role}'"
        )
