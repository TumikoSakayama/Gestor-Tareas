import os
import json
from datetime import date, timedelta
import customtkinter as ctk
from tkinter import messagebox, simpledialog, Toplevel, Listbox, Scrollbar
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass
from TaskApp import TaskApp

if __name__ == "__main__":
    root = ctk.CTk()
    app = TaskApp(root)
    root.mainloop()
