from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.schemas import CodeCollectionCreate, CodeCollectionResponse, CodeCollectionUpdate
from app.services.code import code_service

router = APIRouter(prefix="/code", tags=["code"])


@router.post("/snippets", response_model=CodeCollectionResponse, status_code=status.HTTP_201_CREATED)
def create_snippet(payload: CodeCollectionCreate, db: Session = Depends(get_db)):
    return code_service.create_snippet(db, **payload.model_dump())


@router.get("/snippets", response_model=List[CodeCollectionResponse])
def search_snippets(
    keyword: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    project_name: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    return code_service.search_snippets(db, keyword=keyword, language=language, project_name=project_name)


@router.get("/snippets/{snippet_id}", response_model=CodeCollectionResponse)
def get_snippet(snippet_id: int, db: Session = Depends(get_db)):
    snippet = code_service.get_snippet(db, snippet_id)
    if not snippet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Code snippet not found")
    return snippet


@router.put("/snippets/{snippet_id}", response_model=CodeCollectionResponse)
def update_snippet(snippet_id: int, payload: CodeCollectionUpdate, db: Session = Depends(get_db)):
    snippet = code_service.get_snippet(db, snippet_id)
    if not snippet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Code snippet not found")
    return code_service.update_snippet(db, snippet, **payload.model_dump(exclude_unset=True))


@router.delete("/snippets/{snippet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_snippet(snippet_id: int, db: Session = Depends(get_db)):
    snippet = code_service.get_snippet(db, snippet_id)
    if not snippet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Code snippet not found")
    code_service.delete_snippet(db, snippet)
