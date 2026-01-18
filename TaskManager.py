import json
import os
from datetime import date
from tkinter import messagebox

class TaskManager:
    def __init__(self, file_path="tareas.json"):
        self.file_path = file_path
        self.tasks = []
        self.last_id = 0

        self.load_tasks()

    def load_tasks(self):
        if not os.path.exists(self.file_path):
            self.tasks = []
            self.last_id = 0
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