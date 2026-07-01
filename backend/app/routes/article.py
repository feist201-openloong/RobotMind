from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.schemas import ArticleResponse
from app.services.article import article_service

router = APIRouter(prefix="/articles", tags=["articles"])


class GenerateFromKnowledgeRequest(BaseModel):
    knowledge_entry_id: int


class GenerateFromCodeRequest(BaseModel):
    code_collection_id: int


class UpdateStatusRequest(BaseModel):
    status: str


@router.post("/generate/from-knowledge", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
def generate_from_knowledge(payload: GenerateFromKnowledgeRequest, db: Session = Depends(get_db)):
    try:
        return article_service.generate_article_from_knowledge(db, payload.knowledge_entry_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/generate/from-code", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
def generate_from_code(payload: GenerateFromCodeRequest, db: Session = Depends(get_db)):
    try:
        return article_service.generate_article_from_code(db, payload.code_collection_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/", response_model=List[ArticleResponse])
def list_articles(
    status: Optional[str] = Query(None),
    keyword: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    return article_service.list_articles(db, status=status, keyword=keyword)


@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = article_service.get_article(db, article_id)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    return article


@router.put("/{article_id}/status", response_model=ArticleResponse)
def update_status(article_id: int, payload: UpdateStatusRequest, db: Session = Depends(get_db)):
    try:
        article = article_service.update_article_status(db, article_id, payload.status)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    return article


@router.get("/{article_id}/export/markdown")
def export_markdown(article_id: int, db: Session = Depends(get_db)):
    markdown = article_service.export_article_markdown(db, article_id)
    if not markdown:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    return PlainTextResponse(content=markdown, media_type="text/markdown")
