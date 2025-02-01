from fastapi import FastAPI
import logging
import sys

import log

from jsonbin import JsonBin
from taskobj import Task
import utils

logging.basicConfig(
    stream=sys.stdout,
    level=log.level,
    format=log.fmt,
    datefmt=log.datefmt
)


app = FastAPI()
jsonbin = JsonBin()

bin_id = '679d0cfeacd3cb34a8d61b4f'

@app.get("/tasks")
def get_tasks() -> list[dict]:
    tasks = jsonbin.read_bin(bin_id)['record']
    return tasks

@app.post("/tasks")
def create_task(task: str):
    task_dict = Task.from_string(task).to_dict()
    tasks = jsonbin.read_bin(bin_id)['record']
    tasks.append(task_dict)
    jsonbin.update_bin(bin_id, tasks)


@app.put("/tasks/{task_id}")
def update_task(task_id: int, data: dict):
    tasks = jsonbin.read_bin(bin_id)['record']
    utils.update_item(task_id, data, tasks)
    jsonbin.update_bin(bin_id, tasks)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = jsonbin.read_bin(bin_id)['record']
    utils.delete_item(task_id, tasks)
    jsonbin.update_bin(bin_id, tasks)
