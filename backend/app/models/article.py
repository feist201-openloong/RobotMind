from sqlalchemy import Column, Integer, String, Text, Enum

from app.models.database import Base, TimestampMixin


class Article(Base, TimestampMixin):
    __tablename__ = "generated_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    content = Column(Text, nullable=False)
    markdown_content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    tags = Column(String(500), nullable=True)
    status = Column(
        Enum("draft", "published", name="article_status"),
        nullable=False,
        default="draft",
    )
    word_count = Column(Integer, nullable=False, default=0)
    reading_time = Column(Integer, nullable=False, default=1)  # 分钟
