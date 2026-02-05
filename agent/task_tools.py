# agent/task_tools.py

from sqlalchemy.orm import Session
from models.task import Task
from groq import Groq
import json
import re
client = Groq()


def get_tasks(db: Session, user_id: int):
    tasks = (
        db.query(Task)
        .filter(Task.user_id == user_id)
        .order_by(Task.id.desc())
        .all()
    )

    return [
        {"id": t.id, "title": t.title, "status": t.status}
        for t in tasks
    ]


def create_task(db: Session, user_id: int, title: str, description: str | None):
    task = Task(
        title=title,
        description=description,
        user_id=user_id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
    }


# 🧠 NEW AI FEATURE
def prioritize_tasks(db: Session, user_id: int):
    tasks = (
        db.query(Task)
        .filter(Task.user_id == user_id)
        .order_by(Task.id.desc())
        .all()
    )

    if not tasks:
        return []

    task_data = [
        {
            "id": t.id,
            "title": t.title,
            "description": t.description or "",
        }
        for t in tasks
    ]

    prompt = f"""
You are an assistant that prioritizes tasks.

Return ONLY valid JSON list in this format:
[
  {{
    "id": int,
    "priority_score": 1-10,
    "justification": "one sentence"
  }}
]

Tasks:
{json.dumps(task_data, indent=2)}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    raw = response.choices[0].message.content.strip()

    # 🔧 CLEAN COMMON LLM FORMATTING ISSUES
    raw = re.sub(r"```json|```", "", raw).strip()

    try:
        return json.loads(raw)
    except Exception:
        return {
            "error": "AI response format issue",
            "raw_output": raw  # helpful for debugging
        }
