from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import Task
from src.infrastructure.repositories.tarea_repo import TaskRepository
from auth.dependencies import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/")
def get_tasks(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    repo = TaskRepository(db)
    return repo.get_all(current_user["id"])

@router.post("/")
def create_task(title: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = Task(title=title, owner_id=current_user["id"])
    return TaskRepository(db).create(task)

@router.delete("/{task_id}")
def delete_task(task_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    repo = TaskRepository(db)
    task = repo.get_by_id(task_id)
    if not task or task.owner_id != current_user["id"]:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    repo.delete(task)
    return {"ok": True}