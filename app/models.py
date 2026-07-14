from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


# ── Enums ───────────────────────────────────────────────────────
class TaskStatus(str, Enum):
    """Estados posibles de una tarea."""

    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class TaskPriority(str, Enum):
    """Niveles de prioridad de una tarea."""

    low = "low"
    medium = "medium"
    high = "high"


# ── SQLAlchemy Model ────────────────────────────────────────────
class TaskDB(Base):
    """Modelo de base de datos para tareas."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default=TaskStatus.pending.value)
    priority: Mapped[str] = mapped_column(String(10), default=TaskPriority.medium.value)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )


# ── Pydantic Schemas ───────────────────────────────────────────
class TaskCreate(BaseModel):
    """Schema para crear una tarea."""

    title: str = Field(..., min_length=1, max_length=255, examples=["Configurar CI pipeline"])
    description: str | None = Field(
        None, max_length=1000, examples=["Crear el archivo ci.yml con lint y tests"]
    )
    status: TaskStatus = TaskStatus.pending
    priority: TaskPriority = TaskPriority.medium


class TaskUpdate(BaseModel):
    """Schema para actualizar una tarea (todos los campos opcionales)."""

    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = Field(None, max_length=1000)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None


class TaskResponse(BaseModel):
    """Schema de respuesta para una tarea."""

    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
