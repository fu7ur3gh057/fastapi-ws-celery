from sqlalchemy.orm import Session
import uuid

from app.db.models import Task
from app.schemas.tasks import TaskCreate, TaskUpdate


def get_tasks(db: Session):
    return db.query(Task).all()


def get_task(db: Session, task_id: uuid.UUID):
    return db.query(Task).filter(Task.id == task_id).first()


def create_task(db: Session, task: TaskCreate):
    db_task = Task(title=task.title, description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: uuid.UUID, task_update: TaskUpdate):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        for key, value in task_update.model_dump(exclude_unset=True).items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: uuid.UUID):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task
