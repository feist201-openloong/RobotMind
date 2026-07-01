from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.models.database import Base, TimestampMixin


class LearningPath(Base, TimestampMixin):
    __tablename__ = "learning_paths"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    target_level = Column(String(50), nullable=False, default="beginner")
    status = Column(
        Enum("draft", "active", "completed", name="path_status"),
        nullable=False,
        default="draft",
    )

    tasks = relationship("LearningTask", back_populates="path", cascade="all, delete-orphan")


class LearningTask(Base, TimestampMixin):
    __tablename__ = "learning_tasks"

    id = Column(Integer, primary_key=True, index=True)
    path_id = Column(Integer, ForeignKey("learning_paths.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)
    task_type = Column(String(50), nullable=False, default="reading")
    order = Column(Integer, nullable=False, default=0)
    status = Column(
        Enum("pending", "in_progress", "completed", name="task_status"),
        nullable=False,
        default="pending",
    )

    path = relationship("LearningPath", back_populates="tasks")
    code_snippets = relationship("CodeSnippet", back_populates="task", cascade="all, delete-orphan")


class CodeSnippet(Base, TimestampMixin):
    __tablename__ = "code_snippets"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("learning_tasks.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    code = Column(Text, nullable=False)
    language = Column(String(50), nullable=False, default="python")
    explanation = Column(Text, nullable=True)

    task = relationship("LearningTask", back_populates="code_snippets")


class Article(Base, TimestampMixin):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    tags = Column(String(500), nullable=True)
