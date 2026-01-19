import tkinter as tk
from tkinter import ttk, messagebox

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Do It, JUST DO IT!")
        self.root.geometry("800x600")

        self.manager = TaskManager()

        self.create_widgets()

        self.refresh_table()

    def create_widgets(self):
        input_frame = ttk.LabelFrame(self.root, text="New Task")
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="Description:").grid(row=0, column=0, padx=5, pady=5)
        self.description_entry = ttk.Entry(input_frame, width=30)
        self.description_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Priority:").grid(row=0, column=2, padx=5, pady=5)
        self.priority_combo = ttk.Combobox(input_frame, values=["High", "Medium", "Low"], width=10)
        self.priority_combo.set("Medium")
        self.priority_combo.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5)
        self.category_combo = ttk.Combobox(input_frame, values=["Unespecified", "Study", "Work", "Health", "Financial"])
        self.category_combo.set("Unespecified")
        self.category_combo.grid(row=0, column=5, padx=5, pady=5)

        btn_add = ttk.Button(input_frame, text="Add Task", command=self.add_button)
        btn_add.grid(rwo=0, column=4, padx=10, pady=5)

    def add_button(self):
        description = self.description_entry.get()
        priority = self.priority_combo.get()
        category = self.category_combo.get()

        if not description:
            messagebox.showerror("Error", "The task needs to have a description")
            return
        
        self.manager.add_task(description, priority, category)
        self.update_task_display()
        self.description_entry.delete(0, 'end')