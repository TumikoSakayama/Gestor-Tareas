from TaskManager import TaskManager
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

        self.tree = ttk.Treeview(self.root, columns=("ID", "Desc", "Prio", "Cat", "Status", "End"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Desc", text="Description")
        self.tree.heading("Prio", text="Priority")
        self.tree.heading("Cat", text-"Category")
        self.tree.heading("Status", text="Status")
        self.tree.heading("End", text="Deadline")

        self.tree.column("ID", width=30)
        self.tree.column("Status", width=80)
        self.tree.pack(expand=True, fill="both", padx=10, pady=5)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Mark Completed", command=self.mark_done).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Task", command=self.delete_task).pack(side="left", padx=5)

    def refresh_table(self):
        status = "✅ Done" if task.is_completed else ("⚠️ Expired" if task.is_expired() else "⏳ Pending")

        self.tree.insert("", "end", values=(
            task.task_id,
            task.description,
            task.priority,
            task.category,
            status,
            task.end_date
        ))

    def add_button(self):
        description = self.description_entry.get()
        priority = self.priority_combo.get()
        category = self.category_combo.get()

        if not description:
            messagebox.showerror("Error", "The task needs to have a description")
            return
        
        self.manager.add_task(description, priority, category)
        self.refresh_table()
        self.description_entry.delete(0, tk.END)

    def complete_button(self):
        chosen = self.tree.selection()
        if not chosen:
            return
        
        id_selected = self.tree.item(chosen[0])
        task_id = id_selected['values'][0]

        task = self.manager.find_task_by_id(task_id)
        if task:
            task.mark_done()
            self.manager.save_tasks()
            self.refresh_table()

    def delete_button(self):
        chosen = self.tree.selection()
        if not chosen:
            return
        
        id_selected = self.tree.itme(chosen[0])
        task_id = id_selected['values'][0]

        if messagebox.askyesno("Confirm", f"Delete task {task_id}?"):
            self.manager.delete_task(task_id)
            self.refresh_table()
