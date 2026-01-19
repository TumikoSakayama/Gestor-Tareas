import os
import json
from datetime import date, timedelta
import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Listbox, Scrollbar
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass
from task_app import TaskApp

"""TASK_FILES = "tasks.json"
tasks = []
id_count = 0
today = date.today()

def load_tasks():
    global tasks, id_count
    if os.path.exists(TASK_FILES):
        try:
            with open(TASK_FILES, 'r', encoding='utf-8') as file:
                data = json.load(file)

                if isinstance(data, list):
                    old_tasks = data
                    id_count = max((task["id"] for task in tasks), default=0)
                    messagebox.showinfo("Migration", "OId tasks are being migrated to the new format")
                else:
                    old_tasks = data.get("tasks", [])
                    id_count = data.get("last_id", 0)

                migrated = False
                for task in tasks:
                    if "completion" not in task:
                        task["completion"] = str(date.today())
                        migrated = True
                    
                if migrated:
                    save_tasks()

        except Exception as e:
            messagebox.showerror("File Error", f"Unable to open file: {e}")
    else:
        tasks = []
        id_count = 0


def save_tasks():
    try:
        with open(TASK_FILES, 'w', encoding='utf-8') as file:
            data_to_save = {
                "last_id": last_id,
                "tasks": tasks
            }
            json.dump(data_to_save, file, indent=4, ensure_ascii=False)
            messagebox.showinfo("Succesfull", "Tasks were saved successfully!")
    except Exception as e:
        messagebox.showerror("Save Error", f"Unable to save task at file: {e}")

def add_task():
    global id_count

    description = simpledialog.askstring("New Task", "Task Description: ")
    if not description:
        return
    priority = simpledialog.askstring("Priority", "Priority (Low/Medium/High)") or "Medium"
    priority = priority.capitalize()
    category = simpledialog.askstring("Categoria", "Categoria: ") or "Sin Especificar"

    id_count += 1

    limit_days = {
        "High": 1,
        "Medium": 5,
        "Low": 10
    }

    completion_days = limit_days.get(priority, 2)
    end_date = today + timedelta(days=completion_days)

    new_task = {
        "id": id_count,
        "description": description,
        "priority": priority,
        "category": category.capitalize(),
        "completed": False,
        "date": str(date.today()),
        "completion": str(fecha_limite)
    }

    tasks.append(new_task)
    save_tasks()
    update_task()
    messagebox.showinfo("Successfull", f"Task #{id_count} added successfully!")


def mark_completed():
    chosen = task_list.curseselection()
    if not chosen:
        messagebox.showwarning("Warning", "Please select a task from the list, the one selected does not exist!")
        return

    text = task_list.get(chosen[0])
    id_task= int(text.split(".")[0])
    for task in tasks:
        if task['id'] == id_task:
            task['completed'] = True
            save_tasks()
            update_task()
            messagebox.showinfo("Completed", "Taks has been marked as completed.")
            return

def delete_task():
    global tasks
    chosen = task_list.curseselection()
    if not chosen:
        messagebox.showwarning("Warning", "Select a task to delete (This change can not be undone)")
        return
    
    text = task_list.get(chosen[0])
    id_task = int(text.split(".")[0])

    if messagebox.askyesno("Confirmation", f"Are you sure you want to delete task with #{id_tarea}?"):
        filtered_tasks = [task for task in tasks if task['id'] != id_task]
        save_tasks()
        update_task()

def task_search():
    search_value = simpledialog.askstring("Search", "Enter the search value:")
    if search_value:
        update_task(search_filter=search_value.lower())


def category_filter():
    category = simpledialog.askstring("Filter", "Type the category to filter:")
    if category:
        update_task(cat_filter=category.capitalize())

def update_task(show_tasks=True, search_filter=None, cat_filter=None):
    task_list.delete(0,tk.END)
    for task in tasks:
        if not show_tasks and task["completed"]:
            continue
        if search_filter and search_filter not in task["description"].lower():
            continue
        if cat_filter and cat_filter != task["category"]:
            continue

        finish = date.fromisoformat(task["completion"])
        expired = "⚠️ Expired! :(" if finish < today and not task["completed"] else ""
        status = "✅" if task["completed"] else "⏳"

        row = f"{task["id"]}, {status} {task["description"]} [{task["priority"]}] - {task["category"]} | Vence {task["completion"]} {expired}"
        task_list.insert(tk.END, row)

        if expired:
            task_list.itemconfig(tk.END, {'fg': 'red'})
        elif task["completed"]:
            task_list.itemconfig(tk.END, {'fg': 'gray'})

def main_menu():
    global task_list
    root = tk.Tk()
    root.title("To Do App")
    root.geometry("700x550")
    root.configure(bg="#2c3e50")

    style = {"font": ("Arial", 10, "bold"), "bg": "#34495e", "fg": "white", "relief": "flat", "padx": 10, "pady": 5}

    principal = tk.Frame(root, bg="#1a252f", pady=10)
    principal.pack(fill="x")
    tk.Label(principal, text="MY TASKS", font=("Arial", 18, "bold"), bg="#1a252f", fg="#ecf0f1").pack()


    menu_lateral = tk.Frame(root, bg="#2c3e50", padx=10, pady=10)
    menu_lateral.pack(side="left", fill="y")

    tk.Button(menu_lateral, text="➕ Add New Task", command=add_task, **style).pack(fill="x", pady=5)
    tk.Button(menu_lateral, text="✔ Mark as Completed", command=mark_completed, **style).pack(fill="x", pady=5)
    tk.Button(menu_lateral, text="🔍 Search", command=task_search, **style).pack(fill="x", pady=5)
    tk.Button(menu_lateral, text="📂 By Category", command=category_filter, **style).pack(fill="x", pady=5)
    tk.Button(menu_lateral, text="🔄 Show all", command=lambda: update_task(True), **style).pack(fill="x", pady=5)
    tk.Button(menu_lateral, text="❌ Delete", command=delete_task, bg="#e74c3c", fg="white", font=("Arial", 10, "bold")).pack(fill="x", pady=20)
    tk.Button(menu_lateral, text="🚪 Exit", command=root.destroy, bg="#95a5a6").pack(side="bottom", fill="x")

    frame_lista = tk.Frame(root, bg="#2c3e50", padx=10, pady=10)
    frame_lista.pack(side="right", expand=True, fill="both")

    scrollbar = tk.Scrollbar(frame_lista)
    scrollbar.pack(side="right", fill="y")

    task_list = tk.Listbox(frame_lista, font=("Consolas", 10), bg="#ecf0f1", yscrollcommand=scrollbar.set)
    task_list.pack(expand=True, fill="both")
    scrollbar.config(command=task_list.yview)

    load_tasks()
    update_task()
    
    root.mainloop()"""

if __name__ == "__main__":
    root =tk.Tk()
    app = TaskApp(root)
    root.mainloop()
