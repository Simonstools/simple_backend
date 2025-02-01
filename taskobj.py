import logging
import json
import os

from exception import WrongTaskFormat

class Task:
    def __init__(self, id: int, name: str, status: str):
        self.id = id
        self.name = name
        self.status = status

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
    tasks_filename = 'tasks.json'

    def __init__(self, filename=tasks_filename):
        self.filename = filename
        if os.path.exists(filename) and os.path.isfile(filename):
            pass
        else:
            logging.warning(f"taskfile do not exist, creating new with name {self.filename}")
            with open(self.filename, 'w') as file:
                json.dump(list(), file)

    def get_tasks(self):
        tasks = list()
        with open(self.filename, 'r') as file:
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
        self.__write(tasks)

    def update_task(self, task_id: int):
        tasks = self.get_tasks()
        tasks[task_id].update()
        self.__write(tasks)

    def pop_task(self, task_id: int):
        tasks = self.get_tasks()
        tasks.pop(task_id)
        self.__write(tasks)

    def __write(self, task_list: list):
        new_task_list = list()
        for task in task_list:
            new_task_list.append(task.to_dict())
        with open(self.filename, 'w') as file:
            json.dump(new_task_list, file)