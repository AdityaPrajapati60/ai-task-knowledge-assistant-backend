from typing import Callable, Dict, Any

from agent.task_tools import get_tasks, create_task, prioritize_tasks
from rag.retrieve import retrieve_context
from agent.answer_generator import generate_answer

TOOLS: Dict[str, Callable[..., Any]] = {
    "create_task": create_task,
    "get_tasks": get_tasks,
    "prioritize_tasks": prioritize_tasks,  # 🧠 NEW
    "retrieve_context": retrieve_context,
    "generate_answer": generate_answer,
}
