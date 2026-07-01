from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.code import CodeCollection


class CodeService:
    def create_snippet(self, db: Session, *, title: str, code: str,
                       language: str = "python", description: Optional[str] = None,
                       tags: Optional[str] = None, source_file: Optional[str] = None,
                       project_name: Optional[str] = None, difficulty_level: int = 1) -> CodeCollection:
        snippet = CodeCollection(
            title=title, code=code, language=language,
            description=description, tags=tags, source_file=source_file,
            project_name=project_name, difficulty_level=difficulty_level,
        )
        db.add(snippet)
        db.commit()
        db.refresh(snippet)
        return snippet

    def search_snippets(self, db: Session, *, keyword: Optional[str] = None,
                        language: Optional[str] = None,
                        project_name: Optional[str] = None) -> List[CodeCollection]:
        query = db.query(CodeCollection)
        if keyword:
            like_pattern = f"%{keyword}%"
            query = query.filter(or_(
                CodeCollection.title.ilike(like_pattern),
                CodeCollection.code.ilike(like_pattern),
                CodeCollection.description.ilike(like_pattern),
                CodeCollection.tags.ilike(like_pattern),
            ))
        if language is not None:
            query = query.filter(CodeCollection.language == language)
        if project_name is not None:
            query = query.filter(CodeCollection.project_name == project_name)
        return query.all()

    def get_snippet(self, db: Session, snippet_id: int) -> Optional[CodeCollection]:
        return db.query(CodeCollection).filter(CodeCollection.id == snippet_id).first()

    def update_snippet(self, db: Session, snippet: CodeCollection, **fields) -> CodeCollection:
        for key, value in fields.items():
            if value is not None:
                setattr(snippet, key, value)
        db.commit()
        db.refresh(snippet)
        return snippet

    def delete_snippet(self, db: Session, snippet: CodeCollection) -> None:
        db.delete(snippet)
        db.commit()


code_service = CodeService()
