from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.database import Base, TimestampMixin


class TodoTask(Base, TimestampMixin):
    __tablename__ = "todo_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    priority: Mapped[int] = mapped_column(Integer, default=3)  # 1-5, 1=highest
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, in_progress, completed
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    estimated_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    actual_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    tags: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # comma-separated
    category: Mapped[str] = mapped_column(String(50), default="other")  # learning, coding, research, other
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<TodoTask(id={self.id}, title='{self.title}', status='{self.status}')>"
