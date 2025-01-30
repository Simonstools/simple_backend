from fastapi import FastAPI
import json
import logging
import sys
import os

import log

logging.basicConfig(
    stream=sys.stdout,
    level=log.level,
    format=log.fmt,
    datefmt=log.datefmt
)

class WrongTaskFormat(Exception):
    pass

class Task:
    def __init__(self, id, name, status):
        self.id = id
        self.name = name
        self.status = status

    def update(self):
        pass

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_string(string: str):
        task_dict = dict()
        try:
            task_dict = json.loads(string)
        except json.decoder.JSONDecodeError:
            logging.error(f"Wrong query {string=}, not json format")
            raise WrongTaskFormat
        try:
            task_obj = Task(
                id=task_dict['id'],
                name=task_dict['name'],
                status=task_dict['status']
            )
            return task_obj
        except KeyError:
            logging.error(f"Wrong key found in query {string=}")
            raise WrongTaskFormat


class TaskFile:
    tasks_filename = 'tasks1.json'

    def __init__(self, filename=tasks_filename):
        self.filename = filename
        self.mode = 'r+'
        if os.path.exists(filename) and os.path.isfile(filename):
            pass
        else:
            logging.warning(f"taskfile do not exist, creating new with name {self.filename}")
            with open(self.filename, 'w') as file:
                json.dump(list(), file)

    def get_tasks(self):
        tasks = list()
        with open(self.filename, self.mode) as file:
            for task in json.load(file):
                tasks.append(
                    Task(
                        task['id'],
                        task['name'],
                        task['status']
                    )
                )
        return tasks

    def append_task(self, new_task: Task):
        tasks = self.get_tasks()
        tasks.append(new_task)
        new_task_list = list()
        for task in tasks:
            new_task_list.append(task.to_dict())
        with open(self.filename, self.mode) as file:
            json.dump(new_task_list, file)


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
    tasks = task_file.get_tasks()
    tasks[task_id].update()


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = task_file.get_tasks()
    del tasks[task_id]
