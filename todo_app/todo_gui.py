
import tkinter as tk
from tkinter import messagebox
import json
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.configure(bg="pink")
        self.tasks = []
        self.selected_task_index = None

        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.tasks_file = os.path.join(script_dir, "tasks.json")

        self.load_tasks()

        # --- GUI Components ---
        self.task_frame = tk.Frame(root, bg="pink")
        self.task_frame.pack(pady=5)
        tk.Label(self.task_frame, text="Task:", bg="pink").pack(side=tk.LEFT, padx=5)
        self.task_entry = tk.Entry(self.task_frame, width=40)
        self.task_entry.pack(side=tk.LEFT)

        self.datetime_frame = tk.Frame(root, bg="pink")
        self.datetime_frame.pack(pady=5)

        tk.Label(self.datetime_frame, text="Time:", bg="pink").pack(side=tk.LEFT, padx=5)
        self.year_entry = self.create_time_entry(self.datetime_frame, "YYYY", 4)
        self.month_entry = self.create_time_entry(self.datetime_frame, "MM", 2)
        self.day_entry = self.create_time_entry(self.datetime_frame, "DD", 2)
        self.hour_entry = self.create_time_entry(self.datetime_frame, "HH", 2)
        self.minute_entry = self.create_time_entry(self.datetime_frame, "MM", 2)

        self.button_frame = tk.Frame(root, bg="pink")
        self.button_frame.pack(pady=10)

        self.add_button = tk.Button(self.button_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = tk.Button(self.button_frame, text="Edit Task", command=self.edit_task)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.task_listbox = tk.Listbox(root, width=60, height=15)
        self.task_listbox.pack(pady=10, padx=10)

        self.populate_tasks()

    def create_time_entry(self, parent, placeholder, width):
        entry = tk.Entry(parent, width=width, fg='grey')
        entry.insert(0, placeholder)
        entry.bind('<FocusIn>', lambda e, p=placeholder: self.on_entry_click(e, p))
        entry.bind('<FocusOut>', lambda e, p=placeholder: self.on_focusout(e, p))
        entry.pack(side=tk.LEFT)
        return entry

    def on_entry_click(self, event, placeholder):
        if event.widget.get() == placeholder:
            event.widget.delete(0, "end")
            event.widget.config(fg='black')

    def on_focusout(self, event, placeholder):
        if not event.widget.get():
            event.widget.insert(0, placeholder)
            event.widget.config(fg='grey')

    def add_task(self):
        task = self.task_entry.get()
        if not task or task == "Task":
            messagebox.showwarning("Warning", "You must enter a task.")
            return

        dt = {
            "year": self.year_entry.get(), "month": self.month_entry.get(),
            "day": self.day_entry.get(), "hour": self.hour_entry.get(),
            "minute": self.minute_entry.get()
        }
        for key, value in dt.items():
            if value in ["YYYY", "MM", "DD", "HH"]:
                dt[key] = ""

        if self.selected_task_index is not None:
            self.tasks[self.selected_task_index] = {"task": task, "datetime": dt}
            self.selected_task_index = None
            self.add_button.config(text="Add Task")
        else:
            self.tasks.append({"task": task, "datetime": dt})
        
        self.populate_tasks()
        self.save_tasks()
        self.clear_entries()

    def edit_task(self):
        try:
            self.selected_task_index = self.task_listbox.curselection()[0]
            task_info = self.tasks[self.selected_task_index]
            
            self.clear_entries()
            self.task_entry.insert(0, task_info['task'])
            self.task_entry.config(fg='black') # Ensure text is black

            dt = task_info.get("datetime", {})
            time_entries = {
                self.year_entry: dt.get("year", "YYYY"),
                self.month_entry: dt.get("month", "MM"),
                self.day_entry: dt.get("day", "DD"),
                self.hour_entry: dt.get("hour", "HH"),
                self.minute_entry: dt.get("minute", "MM")
            }

            for entry, value in time_entries.items():
                entry.delete(0, tk.END)
                entry.insert(0, value)
                if value not in ["YYYY", "MM", "DD", "HH"]:
                    entry.config(fg='black')

            self.add_button.config(text="Save Changes")

        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to edit.")

    def delete_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.tasks.pop(selected_task_index)
            self.populate_tasks()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to delete.")

    def clear_entries(self):
        self.task_entry.delete(0, tk.END)
        entries = [self.year_entry, self.month_entry, self.day_entry, self.hour_entry, self.minute_entry]
        placeholders = ["YYYY", "MM", "DD", "HH", "MM"]
        for entry, placeholder in zip(entries, placeholders):
            entry.delete(0, tk.END)
            entry.insert(0, placeholder)
            entry.config(fg='grey')

    def populate_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task_info in self.tasks:
            dt = task_info.get("datetime", {})
            time_str = f"{dt.get('year', '')}-{dt.get('month', '')}-{dt.get('day', '')} {dt.get('hour', '')}:{dt.get('minute', '')}".strip()
            display_text = f"[{time_str}] {task_info['task']}" if time_str and time_str != "- :" else task_info['task']
            self.task_listbox.insert(tk.END, display_text)

    def save_tasks(self):
        with open(self.tasks_file, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def load_tasks(self):
        try:
            with open(self.tasks_file, "r") as f:
                self.tasks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
