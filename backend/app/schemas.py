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
    markdown_content: str
    summary: Optional[str] = None
    tags: Optional[str] = None
    status: str = "draft"
    word_count: int = 0
    reading_time: int = 1


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    markdown_content: Optional[str] = None
    summary: Optional[str] = None
    tags: Optional[str] = None
    status: Optional[str] = None


class ArticleResponse(ArticleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# ── Knowledge Category ──

class KnowledgeCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None
    icon: Optional[str] = None


class KnowledgeCategoryCreate(KnowledgeCategoryBase):
    pass


class KnowledgeCategoryResponse(KnowledgeCategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


# ── Knowledge Entry ──

class KnowledgeEntryBase(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None
    entry_type: str = "concept"
    category_id: Optional[int] = None
    tags: Optional[str] = None
    source_url: Optional[str] = None
    difficulty_level: int = 1
    metadata_json: Optional[str] = None


class KnowledgeEntryCreate(KnowledgeEntryBase):
    pass


class KnowledgeEntryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    entry_type: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[str] = None
    source_url: Optional[str] = None
    difficulty_level: Optional[int] = None
    metadata_json: Optional[str] = None


class KnowledgeEntryResponse(KnowledgeEntryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# ── Code Collection ──

class CodeCollectionBase(BaseModel):
    title: str
    code: str
    language: str = "python"
    description: Optional[str] = None
    tags: Optional[str] = None
    source_file: Optional[str] = None
    project_name: Optional[str] = None
    difficulty_level: int = 1


class CodeCollectionCreate(CodeCollectionBase):
    pass


class CodeCollectionUpdate(BaseModel):
    title: Optional[str] = None
    code: Optional[str] = None
    language: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[str] = None
    source_file: Optional[str] = None
    project_name: Optional[str] = None
    difficulty_level: Optional[int] = None


class CodeCollectionResponse(CodeCollectionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
