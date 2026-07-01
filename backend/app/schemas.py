from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ── Learning Path ──

class LearningPathBase(BaseModel):
    title: str
    description: Optional[str] = None
    target_level: str = "beginner"


class LearningPathCreate(LearningPathBase):
    pass


class LearningPathUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_level: Optional[str] = None
    status: Optional[str] = None


class LearningPathResponse(LearningPathBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    created_at: datetime
    updated_at: datetime


# ── Learning Task ──

class LearningTaskBase(BaseModel):
    title: str
    content: Optional[str] = None
    task_type: str = "reading"
    order: int = 0


class LearningTaskCreate(LearningTaskBase):
    path_id: int


class LearningTaskUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    task_type: Optional[str] = None
    order: Optional[int] = None
    status: Optional[str] = None


class LearningTaskResponse(LearningTaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    path_id: int
    status: str
    created_at: datetime
    updated_at: datetime


# ── Code Snippet ──

class CodeSnippetBase(BaseModel):
    title: str
    code: str
    language: str = "python"
    explanation: Optional[str] = None


class CodeSnippetCreate(CodeSnippetBase):
    task_id: int


class CodeSnippetResponse(CodeSnippetBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    created_at: datetime
    updated_at: datetime


# ── Article ──

class ArticleBase(BaseModel):
    title: str
    content: str
    category: Optional[str] = None
    tags: Optional[str] = None


class ArticleCreate(ArticleBase):
    pass


class ArticleResponse(ArticleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
