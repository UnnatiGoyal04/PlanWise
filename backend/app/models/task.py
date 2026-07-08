from datetime import date
from sqlalchemy import Boolean, Float, String, Date, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base
from app.mixins.audit import AuditMixin

class Task(AuditMixin, Base):
    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint(
            "estimated_hours > 0",
            name="ck_tasks_estimated_hours_positive"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    subject: Mapped[str] = mapped_column(String(100))
    estimated_hours: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )
    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True
    )
    priority: Mapped[str] = mapped_column(String(20))
    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    