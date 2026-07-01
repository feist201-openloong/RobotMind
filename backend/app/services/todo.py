from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from app.models.todo import TodoTask


class TodoService:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, task_data: dict) -> TodoTask:
        task = TodoTask(**task_data)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_tasks(
        self,
        status: Optional[str] = None,
        category: Optional[str] = None,
        priority: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[TodoTask]:
        query = select(TodoTask)

        filters = []
        if status:
            filters.append(TodoTask.status == status)
        if category:
            filters.append(TodoTask.category == category)
        if priority:
            filters.append(TodoTask.priority == priority)

        if filters:
            query = query.where(and_(*filters))

        query = query.order_by(TodoTask.priority, TodoTask.due_date.asc())
        query = query.offset(skip).limit(limit)

        return list(self.db.scalars(query).all())

    def get_task(self, task_id: int) -> Optional[TodoTask]:
        return self.db.get(TodoTask, task_id)

    def update_task_status(self, task_id: int, status: str) -> Optional[TodoTask]:
        task = self.db.get(TodoTask, task_id)
        if not task:
            return None

        task.status = status
        if status == "completed":
            task.completed_at = datetime.now()

        self.db.commit()
        self.db.refresh(task)
        return task

    def smart_schedule(self, available_minutes: int = 480) -> dict:
        now = datetime.now()

        query = select(TodoTask).where(
            and_(
                TodoTask.status.in_(["pending", "in_progress"]),
                TodoTask.estimated_minutes.isnot(None),
            )
        ).order_by(TodoTask.priority, TodoTask.due_date.asc())

        tasks = list(self.db.scalars(query).all())

        scheduled = []
        remaining_minutes = available_minutes
        total_estimated = 0

        for task in tasks:
            estimated = task.estimated_minutes or 0
            if remaining_minutes >= estimated:
                scheduled.append(
                    {
                        "task_id": task.id,
                        "title": task.title,
                        "priority": task.priority,
                        "estimated_minutes": estimated,
                        "due_date": task.due_date.isoformat() if task.due_date else None,
                        "category": task.category,
                    }
                )
                remaining_minutes -= estimated
                total_estimated += estimated
            else:
                break

        return {
            "date": now.strftime("%Y-%m-%d"),
            "available_minutes": available_minutes,
            "scheduled_minutes": total_estimated,
            "remaining_minutes": remaining_minutes,
            "tasks": scheduled,
            "total_tasks": len(scheduled),
        }

    def get_daily_summary(self) -> dict:
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        total_query = select(func.count(TodoTask.id))
        total_tasks = self.db.scalar(total_query) or 0

        completed_today_query = select(func.count(TodoTask.id)).where(
            and_(
                TodoTask.status == "completed",
                TodoTask.completed_at >= today_start,
                TodoTask.completed_at < today_end,
            )
        )
        completed_today = self.db.scalar(completed_today_query) or 0

        pending_query = select(func.count(TodoTask.id)).where(
            TodoTask.status == "pending"
        )
        pending_tasks = self.db.scalar(pending_query) or 0

        in_progress_query = select(func.count(TodoTask.id)).where(
            TodoTask.status == "in_progress"
        )
        in_progress_tasks = self.db.scalar(in_progress_query) or 0

        now = datetime.now()
        overdue_query = select(func.count(TodoTask.id)).where(
            and_(
                TodoTask.status.in_(["pending", "in_progress"]),
                TodoTask.due_date < now,
            )
        )
        overdue_tasks = self.db.scalar(overdue_query) or 0

        category_stats_query = (
            select(TodoTask.category, func.count(TodoTask.id))
            .where(TodoTask.status != "completed")
            .group_by(TodoTask.category)
        )
        category_stats = dict(self.db.scalars(category_stats_query).all())

        priority_stats_query = (
            select(TodoTask.priority, func.count(TodoTask.id))
            .where(TodoTask.status != "completed")
            .group_by(TodoTask.priority)
        )
        priority_stats = dict(self.db.scalars(priority_stats_query).all())

        return {
            "date": today_start.strftime("%Y-%m-%d"),
            "total_tasks": total_tasks,
            "completed_today": completed_today,
            "pending_tasks": pending_tasks,
            "in_progress_tasks": in_progress_tasks,
            "overdue_tasks": overdue_tasks,
            "category_stats": category_stats,
            "priority_stats": priority_stats,
        }
