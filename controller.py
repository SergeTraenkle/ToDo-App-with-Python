from model import Task, DB_Service
from view import TodoView, TaskWidget

class TodoController:
    def __init__(self):
        self.db_service = DB_Service()
        self.view = TodoView(self)
        self.load_tasks()

    def load_tasks(self):
        self.view.tasks = []
        for task in self.db_service.fetchAll():
            self.add_task_widget(task)
        self.update_counter()

    def add_task(self):
        text = self.view.task_input.get().strip()
        if text:
            task = Task(text=text, done=False)
            saved_task = self.db_service.insert(task)
            self.add_task_widget(saved_task)
            self.view.task_input.delete(0, tk.END)
            self.update_counter()

    def add_task_widget(self, task):
        task_widget = TaskWidget(self.view.task_frame, task, self)
        task_widget.pack(fill=tk.X, pady=2)
        self.view.tasks.append(task_widget)

    def update_task(self, task):
        self.db_service.update(task)
        self.update_counter()

    def delete_task(self, task):
        self.db_service.delete(task)
        self.view.tasks = [t for t in self.view.tasks if t.winfo_exists()]
        self.update_counter()

    def update_counter(self):
        open_tasks = sum(1 for task in self.view.tasks
                        if task.winfo_exists() and not task.is_checked())
        self.view.counter_label.config(text=f"Offene Todos: {open_tasks}")

    def run(self):
        self.view.mainloop()

if __name__ == "__main__":
    import tkinter as tk
    app = TodoController()
    app.run()
