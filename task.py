from datetime import date

class Task:
    def __init__(self, task_id, description, priority, category, start_date, end_date, is_completed = False):
        self.task_id = task_id
        self.description = description
        self.priority = priority
        self.category = category
        self.start_date = start_date
        self.end_date = end_date
        self.is_completed = is_completed

    def open_file(self):
        return {
            "id": self.task_id,
            "description": self.description,
            "priority": self.priority,
            "category": self.category,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "is_completed": self.is_completed
        }

    @classmethod
    def task_json(cls, data):
        s_date = date.fromisoformat(data["start_date"])
        e_date = date.fromisoformat(data["end_date"])

        return cls(
            task_id = data["id"],
            description = data["description"],
            priority = data["priority"],
            category = data["category"],
            start_date = s_date,
            end_date = e_date,
            is_completed = data["is_completed"]
        )

    def mark_done(self):
        #We mark a task as completed
        if not self.is_completed:
            self.is_completed = True
            return True
        return False

    def is_expired(self):
        #The task will be mark as expired if we exceed the limit date
        return not self.is_completed and self.end_date < date.today()

