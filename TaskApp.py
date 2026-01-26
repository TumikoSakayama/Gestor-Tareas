from TaskManager import TaskManager
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Do It, JUST DO IT!")
        self.root.geometry("1000x650")

        self.manager = TaskManager()
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        self.input_container = ctk.CTkFrame(self.root)
        self.input_container.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(self.input_container, text="CREATE NEW TASK", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=6, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(self.input_container, text="Description: ").grid(row=1, column=0, padx=5, pady=5)
        self.description_entry = ctk.CTkEntry(self.input_container, width=250, placeholder_text="What is the task to add?")
        self.description_entry.grid(row=1, column=1, padx=5, pady=10)

        ctk.CTkLabel(self.input_container, text="Priority: ").grid(row= 1, column=2, padx=5, pady=5)
        self.priority_combo = ctk.CTkComboBox(self.input_container, values=["High", "Medium", "Low"], width=100)
        self.priority_combo.set("Medium")
        self.priority_combo.grid(row=1, column=3, padx=5, pady=10)

        ctk.CTkLabel(self.input_container, text="Category: ").grid(row=1, column=4, padx=5, pady=5)
        self.category_combo = ctk.CTkComboBox(self.input_container, values=["Unspecified", "Study", "Work", "Health", "Financial"], width=130)
        self.category_combo.set("Unspecified")
        self.category_combo.grid(row=1, column=5, padx=5, pady=10)

        self.btn_add = ctk.CTkButton(self.input_container, text="Add Task", fg_color="#1f538d", command=self.add_button)
        self.btn_add.grid(row=1, column=6, padx=15, pady=10)

        search_frame = ctk.CTkFrame(self.root)
        search_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(search_frame, text="🔍").pack(side="left", padx=10)
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, placeholder_text="Search by description...")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5, pady=8)
        self.search_entry.bind("<KeyRelease>", self.on_search)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TreeView",
        background="#2b2b2b",
        foreground="white",
        fieldbackground="#2b2b2b",
        rowheight=30,
        borderwidth=0)
        style.configure("Treeview.Heading", background="#333333", foreground="white", borderwidth=0)
        style.map("Treeview", background=[('selected', '#1f538d')])

        self.tree = ttk.Treeview(self.root, columns=("ID", "Desc", "Prio", "Cat", "Status", "End"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Desc", text="Description")
        self.tree.heading("Prio", text="Priority")
        self.tree.heading("Cat", text="Category")
        self.tree.heading("Status", text="Status")
        self.tree.heading("End", text="Deadline")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Prio", width=100, anchor="center")
        self.tree.column("Status", width=100, anchor="center")
        self.tree.pack(expand=True, fill="both", padx=20, pady=10)

        btn_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)

        self.btn_complete = ctk.CTkButton(btn_frame, text="Mark as Completed", fg_color="#28a745", hover_color="#218838", command=self.complete_button)
        self.btn_complete.pack(side="left", padx=5)

        self.btn_delete = ctk.CTkButton(btn_frame, text="Delete Task", fg_color="#dc3545", hover_color="#c82333", command=self.delete_button)
        self.btn_delete.pack(side="left", padx=5) 


    def refresh_table(self):
        self.on_search()

    def add_button(self):
        description = self.description_entry.get()
        priority = self.priority_combo.get()
        category = self.category_combo.get()

        if not description:
            messagebox.showerror("Error", "The task needs to have a description")
            return
        
        self.manager.add_task(description, priority, category)
        self.refresh_table()
        self.description_entry.delete(0, ctk.END)

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
            messagebox.showerror("Error", "No task selected")
            return
        
        id_selected = self.tree.item(chosen[0])
        task_id = id_selected['values'][0]

        if messagebox.askyesno("Confirm", f"Delete task {task_id}?"):
            if self.manager.delete_task(task_id):
                self.refresh_table()
            else:
                messagebox.showerror("Error", "Task not found")

    def on_search(self, event=None):
        query = self.search_var.get().strip().lower()

        for i in self.tree.get_children():
            self.tree.delete(i)
            
        for task in self.manager.tasks:
            if query == "" or query in task.description.lower():
                
                if task.is_completed:
                    status = "✅ Done"
                elif task.is_expired():
                    status = "⚠️ Expired"
                else:
                    status = "⏳ Pending"

                self.tree.insert("", "end", values=(
                    task.task_id,
                    task.description,
                    task.priority,
                    task.category,
                    status,
                    task.end_date
                ))
