print("GUI layout initialized")

import tkinter as tk
from tkinter import ttk, simpledialog
from dsa_project.task_manager import TaskManager

class TaskManagerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do Task Manager")
        self.root.geometry("600x400")
        self.task_manager = TaskManager()

        self.create_widgets()
        self.load_tasks()

    def create_widgets(self):
        # Title
        title = ttk.Label(self.root, text="To-Do Task Manager", font=("Arial", 16))
        title.pack(pady=10)


        # Entry frame
        entry_frame = ttk.Frame(self.root)
        entry_frame.pack(pady=5)

        self.task_entry = ttk.Entry(entry_frame, width=40)
        self.task_entry.pack(side=tk.LEFT, padx=5)

        add_button = ttk.Button(entry_frame, text="Add Task", command=self.add_task)
        add_button.pack(side=tk.LEFT)

        # Task List
        self.tree = ttk.Treeview(self.root, columns=("ID", "Task", "Priority"), show='headings', height=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Task", text="Task Description")
        self.tree.heading("Priority", text="Priority")
        self.tree.column("ID", anchor=tk.W, width=50)
        self.tree.column("Task", anchor=tk.W, width=400)
        self.tree.column("Priority", anchor=tk.W, width=100)
        self.tree.pack(pady=10)

        # Button frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=5)

        delete_button = ttk.Button(button_frame, text="Delete Selected", command=self.delete_task)
        delete_button.pack(side=tk.LEFT, padx=5)

        undo_button = ttk.Button(button_frame, text="Undo", command=self.undo)
        undo_button.pack(side=tk.LEFT, padx=5)

        redo_button = ttk.Button(button_frame, text="Redo", command=self.redo)
        redo_button.pack(side=tk.LEFT, padx=5)

    def load_tasks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        tasks = self.task_manager.get_all_tasks_inorder()
        for task in tasks:
            self.tree.insert("", tk.END, values=(task.task_id, task.title, task.priority))

    def add_task(self):
        task = self.task_entry.get()
        if task:
            priority = simpledialog.askinteger("Priority", "Enter task priority", parent=self.root)
            if priority is not None:
                self.task_manager.add_task(task, priority)
                self.task_entry.delete(0, tk.END)
                self.load_tasks()

    def delete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            task_id = item['values'][0]
            priority = item['values'][2]
            self.task_manager.delete_task(task_id, priority)
            self.load_tasks()

    def undo(self):
        self.task_manager.undo()
        self.load_tasks()

    def redo(self):
        self.task_manager.redo()
        self.load_tasks()

# Only run GUI if this is the main file
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerUI(root)
    root.mainloop()
