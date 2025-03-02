from fastapi import WebSocket
from typing import List
from sqlalchemy.orm import Session
import json

from app.db.crud import get_tasks
from app.db.database import SessionLocal
from app.schemas.tasks import TaskResponse


class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        db: Session = SessionLocal()
        tasks = get_tasks(db)
        db.close()
        tasks_json = [TaskResponse(**task.__dict__).model_dump() for task in tasks]
        for task in tasks_json:
            task["id"] = str(task["id"])
        print(json.dumps(tasks_json))
        await websocket.send_text(json.dumps(tasks_json))

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


websocket_manager = WebSocketManager()
