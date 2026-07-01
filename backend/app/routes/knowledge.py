from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.knowledge import KnowledgeCategory, KnowledgeEntry
from app.schemas import (
    KnowledgeCategoryCreate,
    KnowledgeCategoryResponse,
    KnowledgeEntryCreate,
    KnowledgeEntryResponse,
    KnowledgeEntryUpdate,
)
from app.services.knowledge import knowledge_service

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


# ── Categories ──

@router.post("/categories", response_model=KnowledgeCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(payload: KnowledgeCategoryCreate, db: Session = Depends(get_db)):
    return knowledge_service.create_category(db, **payload.model_dump())


@router.get("/categories", response_model=List[KnowledgeCategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return knowledge_service.get_categories(db)


# ── Entries ──

@router.post("/entries", response_model=KnowledgeEntryResponse, status_code=status.HTTP_201_CREATED)
def create_entry(payload: KnowledgeEntryCreate, db: Session = Depends(get_db)):
    return knowledge_service.create_entry(db, **payload.model_dump())


@router.get("/entries", response_model=List[KnowledgeEntryResponse])
def search_entries(
    keyword: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    entry_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    return knowledge_service.search_entries(db, keyword=keyword, category_id=category_id, entry_type=entry_type)


@router.get("/entries/{entry_id}", response_model=KnowledgeEntryResponse)
def get_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = knowledge_service.get_entry(db, entry_id)
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Knowledge entry not found")
    return entry


@router.put("/entries/{entry_id}", response_model=KnowledgeEntryResponse)
def update_entry(entry_id: int, payload: KnowledgeEntryUpdate, db: Session = Depends(get_db)):
    entry = knowledge_service.get_entry(db, entry_id)
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Knowledge entry not found")
    return knowledge_service.update_entry(db, entry, **payload.model_dump(exclude_unset=True))
