from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.schemas import (
    TodoDailySummary,
    TodoScheduleResponse,
    TodoTaskCreate,
    TodoTaskResponse,
    TodoTaskStatusUpdate,
)
from app.services.todo import TodoService

router = APIRouter(prefix="/todo", tags=["Todo"])


@router.post("/tasks/", response_model=TodoTaskResponse, status_code=201)
def create_task(task_data: TodoTaskCreate, db: Session = Depends(get_db)):
    service = TodoService(db)
    task = service.create_task(task_data.model_dump())
    return task


@router.get("/tasks/", response_model=list[TodoTaskResponse])
def get_tasks(
    status: Optional[str] = Query(None, description="Filter by status"),
    category: Optional[str] = Query(None, description="Filter by category"),
    priority: Optional[int] = Query(None, description="Filter by priority"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    service = TodoService(db)
    tasks = service.get_tasks(
        status=status, category=category, priority=priority, skip=skip, limit=limit
    )
    return tasks


@router.get("/tasks/{task_id}", response_model=TodoTaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    service = TodoService(db)
    task = service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}/status", response_model=TodoTaskResponse)
def update_task_status(
    task_id: int,
    status_update: TodoTaskStatusUpdate,
    db: Session = Depends(get_db),
):
    service = TodoService(db)
    task = service.update_task_status(task_id, status_update.status)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/schedule/", response_model=TodoScheduleResponse)
def get_schedule(
    available_minutes: int = Query(480, ge=1, le=1440, description="Available minutes in a day"),
    db: Session = Depends(get_db),
):
    service = TodoService(db)
    schedule = service.smart_schedule(available_minutes=available_minutes)
    return schedule


@router.get("/summary/", response_model=TodoDailySummary)
def get_summary(db: Session = Depends(get_db)):
    service = TodoService(db)
    summary = service.get_daily_summary()
    return summary
