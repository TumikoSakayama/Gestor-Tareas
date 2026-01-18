class TaskManager:
    def __init__(self, file_path="tareas.json"):
        self.file_path = file_path
        self.tasks = []
        self.last_id = 0

        self.load_tasks()
