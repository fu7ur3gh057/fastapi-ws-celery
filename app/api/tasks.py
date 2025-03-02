import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from app.scheduler.tasks import send_report

from app.db.crud import get_tasks, get_task, create_task, update_task, delete_task
from app.db.database import get_db
from app.schemas.tasks import TaskResponse, TaskCreate, TaskUpdate
from app.ws.manager import websocket_manager


router = APIRouter(prefix="/tasks", tags=["tasks"])

async def tasks_broadcasting(db):
    tasks = get_tasks(db)
    tasks_json = [TaskResponse(**t.__dict__).model_dump() for t in tasks]
    for task in tasks_json:
        task["id"] = str(task["id"])
    await websocket_manager.broadcast(json.dumps(tasks_json))

@router.get("/", response_model=list[TaskResponse])
async def read_tasks(db: Session = Depends(get_db)):
    return get_tasks(db)

@router.get("/{task_id}", response_model=TaskResponse)
async def read_task(task_id: uuid.UUID, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/", response_model=TaskResponse)
async def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = create_task(db, task)
    await tasks_broadcasting(db)
    return new_task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_existing_task(task_id: uuid.UUID, task_update: TaskUpdate, db: Session = Depends(get_db)):
    if task_update.title is not None and len(task_update.title) == 0:
        raise HTTPException(status_code=404, detail="Title cannot be empty")
    task = update_task(db, task_id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await tasks_broadcasting(db)
    return task

@router.delete("/{task_id}")
async def delete_existing_task(task_id: uuid.UUID, db: Session = Depends(get_db)):
    task = delete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await tasks_broadcasting(db)
    return {"message": "Task deleted"}


@router.post("/send-report")
async def send_report_endpoint(email: str):
    task = send_report.delay(email)
    return {"task_id": task.id, "message": f"Report is being sent to {email}"}