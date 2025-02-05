import tkinter as tk
from tkinter import ttk
from model import Task

class TaskWidget(tk.Frame):
    def __init__(self, parent, task: Task, callback):
        super().__init__(parent)
        self.task = task
        self.callback = callback

        self.checked = tk.BooleanVar(value=task.done)
        self.checkbox = ttk.Checkbutton(self, variable=self.checked,
                                      command=self.on_checkbox_click)
        self.checkbox.pack(side=tk.LEFT)

        self.label = ttk.Label(self, text=task.text)
        self.label.pack(side=tk.LEFT, padx=5)

        self.delete_btn = ttk.Button(self, text="❌", width=3,
                                   command=self.on_delete_click)
        self.delete_btn.pack(side=tk.RIGHT)

    def on_checkbox_click(self):
        self.task.done = self.checked.get()
        self.callback.update_task(self.task)

    def on_delete_click(self):
        self.callback.delete_task(self.task)
        self.destroy()

    def is_checked(self):
        return self.checked.get()

class TodoView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Todo App mit DB")
        self.geometry("400x600+400+300")
        self.tasks = []
        self.setup_gui()

    def setup_gui(self):
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=10, padx=10, fill=tk.X)

        self.task_input = ttk.Entry(input_frame)
        self.task_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        add_btn = ttk.Button(input_frame, text="Hinzufügen",
                           command=self.controller.add_task)
        add_btn.pack(side=tk.RIGHT)

        self.task_frame = ttk.Frame(self)
        self.task_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.counter_label = ttk.Label(self, text="Offene Todos: 0")
        self.counter_label.pack(pady=5)
