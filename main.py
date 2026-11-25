from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

tasks = [
    {"id": 1, "title": "Set up FastAPI", "done": True}
    {"id": 2, "title": "Build a CRUD endpoints", "done": False},
    {"id": 3, "title": "Push to GitHub", "done": False},
]

@app.get("/")
def root():
    return {"name": "Task API!", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health():
    return {"status": "ok"}

def error(status: int, message: str):
    return JSONResponse(status_code=status, content={"error": message})


def find_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

@app.get("/tasks")
def list_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        return error(404, f"Task {task_id} not found")
    return task