from datetime import date, datetime

from sqlalchemy import Boolean, Float, String, Date, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Task(Base):
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
    estimated_hours: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(String(1000))
    priority: Mapped[str] = mapped_column(String(20))
    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )