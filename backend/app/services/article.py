import re
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.article import Article
from app.models.knowledge import KnowledgeEntry
from app.models.code import CodeCollection


class ArticleService:
    def generate_article_from_knowledge(
        self, db: Session, knowledge_entry_id: int
    ) -> Article:
        entry = db.query(KnowledgeEntry).filter(KnowledgeEntry.id == knowledge_entry_id).first()
        if not entry:
            raise ValueError("Knowledge entry not found")

        title = f"学习笔记: {entry.title}"
        content = entry.content
        markdown_content = self._generate_markdown_from_knowledge(entry)
        summary = entry.summary or f"关于{entry.title}的学习笔记"
        tags = entry.tags or "学习笔记"
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
        db.commit()
        db.refresh(article)
        return article

    def generate_article_from_code(
        self, db: Session, code_collection_id: int
    ) -> Article:
        code_entry = db.query(CodeCollection).filter(CodeCollection.id == code_collection_id).first()
        if not code_entry:
            raise ValueError("Code collection not found")

        title = f"代码解析: {code_entry.title}"
        content = code_entry.description or code_entry.title
        markdown_content = self._generate_markdown_from_code(code_entry)
        summary = code_entry.description or f"关于{code_entry.title}的代码解析"
        tags = code_entry.tags or "代码解析"
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
        db.commit()
        db.refresh(article)
        return article

    def get_article(self, db: Session, article_id: int) -> Optional[Article]:
        return db.query(Article).filter(Article.id == article_id).first()

    def list_articles(
        self, db: Session, status: Optional[str] = None, keyword: Optional[str] = None
    ) -> List[Article]:
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
        if status not in ("draft", "published"):
            raise ValueError("Invalid status. Must be 'draft' or 'published'")

        article = self.get_article(db, article_id)
        if not article:
            return None

        article.status = status
        db.commit()
        db.refresh(article)
        return article

    def export_article_markdown(
        self, db: Session, article_id: int
    ) -> Optional[str]:
        article = self.get_article(db, article_id)
        if not article:
            return None
        return article.markdown_content

    def _generate_markdown_from_knowledge(self, entry: KnowledgeEntry) -> str:
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
