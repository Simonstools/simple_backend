from fastapi import FastAPI
import logging
import sys

import log

from taskobj import TaskFile, Task

logging.basicConfig(
    stream=sys.stdout,
    level=log.level,
    format=log.fmt,
    datefmt=log.datefmt
)


app = FastAPI()
task_file = TaskFile()


@app.get("/tasks")
def get_tasks() -> list[dict]:
    tasks = [task.to_dict() for task in task_file.get_tasks()]
    return tasks

@app.post("/tasks")
def create_task(task: str):
    task_obj = Task.from_string(task)
    task_file.append_task(task_obj)


@app.put("/tasks/{task_id}")
def update_task(task_id: int):
    task_file.update_task(task_id)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    task_file.pop_task(task_id)
