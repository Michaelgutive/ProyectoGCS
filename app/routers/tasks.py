from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import TaskCreate, TaskDB, TaskPriority, TaskResponse, TaskStatus, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    skip: int = 0,
    limit: int = 100,
    status_filter: TaskStatus | None = None,
    db: Session = Depends(get_db),
):
    """Obtener todas las tareas con paginación, con filtro opcional por estado."""
    query = db.query(TaskDB)
    if status_filter is not None:
        query = query.filter(TaskDB.status == status_filter.value)
    return query.offset(skip).limit(limit).all()


@router.get("/stats/summary")
def get_tasks_stats(db: Session = Depends(get_db)):
    """Obtener un resumen de tareas agrupadas por estado y prioridad."""
    tasks = db.query(TaskDB).all()

    by_status = {status_value.value: 0 for status_value in TaskStatus}
    by_priority = {priority_value.value: 0 for priority_value in TaskPriority}

    for task in tasks:
        by_status[task.status] = by_status.get(task.status, 0) + 1
        by_priority[task.priority] = by_priority.get(task.priority, 0) + 1

    return {
        "total_tasks": len(tasks),
        "by_status": by_status,
        "by_priority": by_priority,
    }


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Obtener una tarea por su ID."""
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    return task


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Crear una nueva tarea."""
    db_task = TaskDB(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    """Actualizar una tarea existente."""
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    update_data = task.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Eliminar una tarea por su ID."""
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    db.delete(db_task)
    db.commit()
