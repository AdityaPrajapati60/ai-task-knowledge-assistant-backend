from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db.database import SessionLocal
from models.user import User as UserModel
from models.task import Task
from models.schemas import TaskCreate, TaskResponse, TaskUpdate
from api.auth_helpers import get_current_user
from agent.task_tools import prioritize_tasks

router = APIRouter(tags=["tasks"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------------------------------------------------------
# 1. CREATE TASK (POST)
# ----------------------------------------------------------------------
@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    new = Task(**payload.dict(), user_id=current_user.id)
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


# ----------------------------------------------------------------------
# 2. LIST TASKS
# ----------------------------------------------------------------------
@router.get("/tasks", response_model=List[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
    limit: int = 10,
    offset: int = 0,
):
    return (
        db.query(Task)
        .filter(Task.user_id == current_user.id)
        .order_by(Task.id.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )


# ----------------------------------------------------------------------
# 🧠 AI TASK PRIORITIZATION (STATIC ROUTE FIRST)
# ----------------------------------------------------------------------
@router.get("/tasks/prioritize")
def ai_prioritize_tasks(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return prioritize_tasks(db, current_user.id)


# ----------------------------------------------------------------------
# 3. GET SINGLE TASK
# ----------------------------------------------------------------------
@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    t = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()

    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    return t


# ----------------------------------------------------------------------
# 4. UPDATE TASK
# ----------------------------------------------------------------------
@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    t = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()

    if not t:
        raise HTTPException(status_code=404, detail="Task not found")

    if payload.title is not None:
        t.title = payload.title.strip()
    if payload.description is not None:
        t.description = payload.description
    if payload.status is not None:
        t.status = payload.status.value

    db.commit()
    db.refresh(t)
    return t


# ----------------------------------------------------------------------
# 5. DELETE TASK
# ----------------------------------------------------------------------
@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    t = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()

    if not t:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(t)
    db.commit()
    return
