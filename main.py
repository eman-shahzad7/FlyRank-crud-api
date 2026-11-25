from typing import Optional

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Task API", version="1.0")

# In-memory "database": gone when the server restarts
tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build a CRUD API", "done": False},
    {"id": 3, "title": "Push to GitHub", "done": False},
]


class TaskCreate(BaseModel):
    title: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


def error(status: int, message: str):
    return JSONResponse(status_code=status, content={"error": message})


def find_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


@app.get("/")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        return error(404, f"Task {task_id} not found")
    return task


@app.post("/tasks", status_code=201)
def create_task(body: TaskCreate):
    if body.title is None or not body.title.strip():
        return error(400, "title is required and cannot be empty")
    next_id = max((t["id"] for t in tasks), default=0) + 1
    task = {"id": next_id, "title": body.title.strip(), "done": False}
    tasks.append(task)
    return task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, body: TaskUpdate):
    task = find_task(task_id)
    if task is None:
        return error(404, f"Task {task_id} not found")
    if body.title is None and body.done is None:
        return error(400, "send at least one of: title, done")
    if body.title is not None:
        if not body.title.strip():
            return error(400, "title cannot be empty")
        task["title"] = body.title.strip()
    if body.done is not None:
        task["done"] = body.done
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        return error(404, f"Task {task_id} not found")
    tasks.remove(task)
    return Response(status_code=204)