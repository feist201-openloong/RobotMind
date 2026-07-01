from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.knowledge import KnowledgeCategory, KnowledgeEntry


def create_category(db: Session, *, name: str, description: Optional[str] = None,
                    parent_id: Optional[int] = None, icon: Optional[str] = None) -> KnowledgeCategory:
    category = KnowledgeCategory(name=name, description=description,
                                 parent_id=parent_id, icon=icon)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_categories(db: Session) -> List[KnowledgeCategory]:
    return db.query(KnowledgeCategory).all()


def create_entry(db: Session, *, title: str, content: str,
                 summary: Optional[str] = None, entry_type: str = "concept",
                 category_id: Optional[int] = None, tags: Optional[str] = None,
                 source_url: Optional[str] = None, difficulty_level: int = 1,
                 metadata_json: Optional[str] = None) -> KnowledgeEntry:
    entry = KnowledgeEntry(
        title=title, content=content, summary=summary,
        entry_type=entry_type, category_id=category_id,
        tags=tags, source_url=source_url,
        difficulty_level=difficulty_level, metadata_json=metadata_json,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def search_entries(db: Session, *, keyword: Optional[str] = None,
                   category_id: Optional[int] = None,
                   entry_type: Optional[str] = None) -> List[KnowledgeEntry]:
    query = db.query(KnowledgeEntry)
    if keyword:
        like_pattern = f"%{keyword}%"
        query = query.filter(or_(
            KnowledgeEntry.title.ilike(like_pattern),
            KnowledgeEntry.content.ilike(like_pattern),
            KnowledgeEntry.tags.ilike(like_pattern),
        ))
    if category_id is not None:
        query = query.filter(KnowledgeEntry.category_id == category_id)
    if entry_type is not None:
        query = query.filter(KnowledgeEntry.entry_type == entry_type)
    return query.all()


def get_entry(db: Session, entry_id: int) -> Optional[KnowledgeEntry]:
    return db.query(KnowledgeEntry).filter(KnowledgeEntry.id == entry_id).first()


def update_entry(db: Session, entry: KnowledgeEntry, **fields) -> KnowledgeEntry:
    for key, value in fields.items():
        if value is not None:
            setattr(entry, key, value)
    db.commit()
    db.refresh(entry)
    return entry
