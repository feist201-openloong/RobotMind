import re
import html
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.article import Article
from app.models.knowledge import KnowledgeEntry
from app.models.code import CodeCollection

# Patterns that indicate potential XSS payloads
_XSS_PATTERNS = [
    re.compile(r"<script\b", re.IGNORECASE),
    re.compile(r"javascript:", re.IGNORECASE),
    re.compile(r"on\w+\s*=", re.IGNORECASE),
    re.compile(r"<iframe\b", re.IGNORECASE),
    re.compile(r"<object\b", re.IGNORECASE),
    re.compile(r"<embed\b", re.IGNORECASE),
    re.compile(r"<form\b", re.IGNORECASE),
    re.compile(r"<link\b", re.IGNORECASE),
    re.compile(r"<meta\b", re.IGNORECASE),
    re.compile(r"<style\b", re.IGNORECASE),
    re.compile(r"<svg\b", re.IGNORECASE),
    re.compile(r"expression\s*\(", re.IGNORECASE),
    re.compile(r"url\s*\(", re.IGNORECASE),
]


def _sanitize_xss(text: str) -> str:
    """Sanitize text to prevent XSS attacks while preserving markdown structure.

    Escapes HTML special characters and strips dangerous patterns.
    """
    if not text:
        return text

    for pattern in _XSS_PATTERNS:
        text = pattern.sub("", text)

    text = html.escape(text, quote=False)

    # Restore safe markdown patterns: bold, italic, code blocks, headings, links
    # These are safe because they don't execute scripts
    text = re.sub(r"\*\*(.+?)\*\*", r"**\1**", text)
    text = re.sub(r"\*(.+?)\*", r"*\1*", text)
    text = re.sub(r"`(.+?)`", r"`\1`", text)
    text = re.sub(r"^(#{1,6})\s", r"\1 ", text, flags=re.MULTILINE)

    return text


class ArticleService:
    def generate_article_from_knowledge(
        self, db: Session, knowledge_entry_id: int
    ) -> Article:
        """Generate an article from a knowledge entry."""
        if not isinstance(knowledge_entry_id, int) or knowledge_entry_id <= 0:
            raise ValueError("Invalid knowledge_entry_id: must be a positive integer")

        entry = db.query(KnowledgeEntry).filter(KnowledgeEntry.id == knowledge_entry_id).first()
        if not entry:
            raise ValueError("Knowledge entry not found")

        title = f"学习笔记: {entry.title}"
        content = entry.content
        markdown_content = self._generate_markdown_from_knowledge(entry)
        summary = entry.summary or f"关于{entry.title}的学习笔记"
        tags = entry.tags or "学习笔记"

        return self._create_article(db, title, content, markdown_content, summary, tags)

    def generate_article_from_code(
        self, db: Session, code_collection_id: int
    ) -> Article:
        """Generate an article from a code collection."""
        if not isinstance(code_collection_id, int) or code_collection_id <= 0:
            raise ValueError("Invalid code_collection_id: must be a positive integer")

        code_entry = db.query(CodeCollection).filter(CodeCollection.id == code_collection_id).first()
        if not code_entry:
            raise ValueError("Code collection not found")

        title = f"代码解析: {code_entry.title}"
        content = code_entry.description or code_entry.title
        markdown_content = self._generate_markdown_from_code(code_entry)
        summary = code_entry.description or f"关于{code_entry.title}的代码解析"
        tags = code_entry.tags or "代码解析"

        return self._create_article(db, title, content, markdown_content, summary, tags)

    def get_article(self, db: Session, article_id: int) -> Optional[Article]:
        """Retrieve a single article by ID."""
        if not isinstance(article_id, int) or article_id <= 0:
            raise ValueError("Invalid article_id: must be a positive integer")
        return db.query(Article).filter(Article.id == article_id).first()

    def list_articles(
        self, db: Session, status: Optional[str] = None, keyword: Optional[str] = None
    ) -> List[Article]:
        """List articles with optional status and keyword filters."""
        query = db.query(Article)
        if status:
            query = query.filter(Article.status == status)
        if keyword:
            like_pattern = f"%{keyword}%"
            query = query.filter(
                (Article.title.ilike(like_pattern)) | (Article.tags.ilike(like_pattern))
            )
        return query.order_by(Article.created_at.desc()).all()

    def update_article_status(
        self, db: Session, article_id: int, status: str
    ) -> Optional[Article]:
        """Update the status of an article (draft or published)."""
        if status not in ("draft", "published"):
            raise ValueError("Invalid status. Must be 'draft' or 'published'")

        article = self.get_article(db, article_id)
        if not article:
            return None

        article.status = status
        try:
            db.commit()
            db.refresh(article)
        except Exception:
            db.rollback()
            raise
        return article

    def export_article_markdown(
        self, db: Session, article_id: int
    ) -> Optional[str]:
        """Export the markdown content of an article."""
        article = self.get_article(db, article_id)
        if not article:
            return None
        return article.markdown_content

    def _create_article(
        self, db: Session, title: str, content: str, markdown_content: str,
        summary: str, tags: str
    ) -> Article:
        """Create and persist a new article with common logic."""
        content = _sanitize_xss(content)
        markdown_content = _sanitize_xss(markdown_content)
        summary = _sanitize_xss(summary)
        tags = _sanitize_xss(tags)
        title = _sanitize_xss(title)

        word_count = len(content)
        reading_time = max(1, word_count // 500)

        article = Article(
            title=title,
            content=content,
            markdown_content=markdown_content,
            summary=summary,
            tags=tags,
            status="draft",
            word_count=word_count,
            reading_time=reading_time,
        )
        db.add(article)
        try:
            db.commit()
            db.refresh(article)
        except Exception:
            db.rollback()
            raise
        return article

    def _generate_markdown_from_knowledge(self, entry: KnowledgeEntry) -> str:
        """Generate markdown content from a knowledge entry."""
        lines = [
            f"# {entry.title}",
            "",
            f"**类型**: {entry.entry_type}",
            f"**难度等级**: {entry.difficulty_level}",
            "",
            "## 内容",
            "",
            entry.content,
        ]
        if entry.tags:
            lines.extend(["", f"**标签**: {entry.tags}"])
        return "\n".join(lines)

    def _generate_markdown_from_code(self, code_entry: CodeCollection) -> str:
        """Generate markdown content from a code collection."""
        lines = [
            f"# {code_entry.title}",
            "",
            f"**语言**: {code_entry.language}",
        ]
        if code_entry.project_name:
            lines.append(f"**项目**: {code_entry.project_name}")
        lines.extend([
            "",
            "## 代码",
            "",
            f"```{code_entry.language}",
            code_entry.code,
            "```",
        ])
        if code_entry.description:
            lines.extend(["", "## 说明", "", code_entry.description])
        if code_entry.tags:
            lines.extend(["", f"**标签**: {code_entry.tags}"])
        return "\n".join(lines)


article_service = ArticleService()
