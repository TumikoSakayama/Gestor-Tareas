from task import Task
import json
import os
import sys
from datetime import date, timedelta
from tkinter import messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TASK_FILE = os.path.join(BASE_DIR, "tareas.json")

class TaskManager:
    def __init__(self, file_path=DEFAULT_TASK_FILE):
        self.file_path = file_path
        self.tasks = []
        self.last_id = 0

        self.load_tasks()

    def load_tasks(self):
        if not os.path.exists(self.file_path):
            return
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                json_tasks = data.get("tasks", [])
                self.last_id = data.get("last_id", 0)

                self.tasks = []
                for task in json_tasks:
                    task_object = Task.task_json(task)
                    self.tasks.append(task_object)
        
        except (json.JSONDecodeError, KeyError):
            self.tasks = []
            self.last_id = 0

    def save_tasks(self):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                task_list = [task.open_file() for task in self.tasks]

                tasks_to_save = {
                    "last_id": self.last_id,
                    "tasks": task_list 
                }

                json.dump(tasks_to_save, file, indent=4, ensure_ascii=False)

        except Exception as e:
            messagebox.showerror("Save Error", f"Unable to save task at file: {e}")

    def add_task(self, description, priority, category):
        priorities = {
            "High": 1,
            "Medium": 5,
            "Low": 10
        }
        days_to_add = priorities.get(priority, 2)

        today = date.today()
        limit_date = today + timedelta(days=days_to_add)

        self.last_id += 1

        new_task = Task(
            task_id = self.last_id,
            description = description,
            priority = priority,
            category = category,
            start_date = today,
            end_date = limit_date
        )

        self.tasks.append(new_task)
        self.save_tasks()
        return new_task

    def find_task_by_id(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def search(self, value):
        value = value.lower()
        results = [task for task in self.tasks if task in task.description.lower()]
        return results


    def delete_task(self, task_id):
        task = self.find_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            return True
        return False