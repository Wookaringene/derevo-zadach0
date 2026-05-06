from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from contextlib import asynccontextmanager

from .database import (
    init_db, get_all_tasks, get_task,
    create_task, update_status, delete_task
)

# Модели данных
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    created_at: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("✅ База данных готова")
    yield

app = FastAPI(title="Task Board API", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Task Board API", "endpoints": ["/tasks", "/tasks/{id}"]}

@app.get("/tasks", response_model=List[TaskResponse])
async def list_tasks():
    """Получить все задачи"""
    return await get_all_tasks()

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task_by_id(task_id: int):
    """Получить задачу по ID"""
    task = await get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks")
async def create_new_task(task: TaskCreate):
    """Создать задачу"""
    task_id = await create_task(task.title, task.description)
    return {"id": task_id, "message": "Task created"}

@app.patch("/tasks/{task_id}/status")
async def change_status(task_id: int, status: str):
    """Изменить статус (pending/in_progress/completed)"""
    task = await get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await update_status(task_id, status)
    return {"message": f"Status changed to {status}"}

@app.delete("/tasks/{task_id}")
async def delete_task_by_id(task_id: int):
    """Удалить задачу"""
    task = await get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await delete_task(task_id)
    return {"message": "Task deleted"}