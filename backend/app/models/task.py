from datetime import date

from sqlalchemy import Boolean, Float, String, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    subject: Mapped[str] = mapped_column(String(100))
    estimated_hours: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(String(1000))
    priority: Mapped[str] = mapped_column(String(20))
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)