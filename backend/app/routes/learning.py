from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.learning import LearningPath, LearningTask
from app.schemas import (
    LearningPathCreate,
    LearningPathResponse,
    LearningPathUpdate,
    LearningTaskCreate,
    LearningTaskResponse,
    LearningTaskUpdate,
)

router = APIRouter(prefix="/learning", tags=["learning"])


# ── Learning Paths ──

@router.get("/paths", response_model=List[LearningPathResponse])
def list_paths(db: Session = Depends(get_db)):
    return db.query(LearningPath).all()


@router.get("/paths/{path_id}", response_model=LearningPathResponse)
def get_path(path_id: int, db: Session = Depends(get_db)):
    path = db.query(LearningPath).filter(LearningPath.id == path_id).first()
    if not path:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning path not found")
    return path


@router.post("/paths", response_model=LearningPathResponse, status_code=status.HTTP_201_CREATED)
def create_path(payload: LearningPathCreate, db: Session = Depends(get_db)):
    path = LearningPath(**payload.model_dump())
    db.add(path)
    db.commit()
    db.refresh(path)
    return path


@router.put("/paths/{path_id}", response_model=LearningPathResponse)
def update_path(path_id: int, payload: LearningPathUpdate, db: Session = Depends(get_db)):
    path = db.query(LearningPath).filter(LearningPath.id == path_id).first()
    if not path:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning path not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(path, key, value)
    db.commit()
    db.refresh(path)
    return path


@router.delete("/paths/{path_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_path(path_id: int, db: Session = Depends(get_db)):
    path = db.query(LearningPath).filter(LearningPath.id == path_id).first()
    if not path:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning path not found")
    db.delete(path)
    db.commit()


# ── Learning Tasks ──

@router.get("/tasks", response_model=List[LearningTaskResponse])
def list_tasks(path_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(LearningTask)
    if path_id is not None:
        query = query.filter(LearningTask.path_id == path_id)
    return query.order_by(LearningTask.order).all()


@router.get("/tasks/{task_id}", response_model=LearningTaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(LearningTask).filter(LearningTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning task not found")
    return task


@router.post("/tasks", response_model=LearningTaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: LearningTaskCreate, db: Session = Depends(get_db)):
    path = db.query(LearningPath).filter(LearningPath.id == payload.path_id).first()
    if not path:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent learning path not found")
    task = LearningTask(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.put("/tasks/{task_id}", response_model=LearningTaskResponse)
def update_task(task_id: int, payload: LearningTaskUpdate, db: Session = Depends(get_db)):
    task = db.query(LearningTask).filter(LearningTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning task not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


@router.patch("/tasks/{task_id}/status", response_model=LearningTaskResponse)
def update_task_status(task_id: int, status_value: str, db: Session = Depends(get_db)):
    allowed = {"pending", "in_progress", "completed"}
    if status_value not in allowed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid status. Allowed: {allowed}")
    task = db.query(LearningTask).filter(LearningTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning task not found")
    task.status = status_value
    db.commit()
    db.refresh(task)
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(LearningTask).filter(LearningTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning task not found")
    db.delete(task)
    db.commit()
