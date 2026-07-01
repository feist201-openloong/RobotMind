from sqlalchemy import Column, Integer, String, Text

from app.models.database import Base, TimestampMixin


class CodeCollection(Base, TimestampMixin):
    __tablename__ = "code_collections"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    code = Column(Text, nullable=False)
    language = Column(String(50), nullable=False, default="python")
    description = Column(Text, nullable=True)
    tags = Column(String(500), nullable=True)
    source_file = Column(String(500), nullable=True)
    project_name = Column(String(200), nullable=True)
    difficulty_level = Column(Integer, nullable=False, default=1)
