from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.models.database import Base, TimestampMixin


class KnowledgeCategory(Base, TimestampMixin):
    __tablename__ = "knowledge_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey("knowledge_categories.id"), nullable=True)
    icon = Column(String(50), nullable=True)

    parent = relationship("KnowledgeCategory", remote_side=[id], backref="children")
    entries = relationship("KnowledgeEntry", back_populates="category", cascade="all, delete-orphan")


class KnowledgeEntry(Base, TimestampMixin):
    __tablename__ = "knowledge_entries"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    entry_type = Column(String(50), nullable=False, default="concept")
    category_id = Column(Integer, ForeignKey("knowledge_categories.id"), nullable=True)
    tags = Column(String(500), nullable=True)
    source_url = Column(String(500), nullable=True)
    difficulty_level = Column(Integer, nullable=False, default=1)
    metadata_json = Column(Text, nullable=True, name="metadata")

    category = relationship("KnowledgeCategory", back_populates="entries")
