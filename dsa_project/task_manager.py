import sqlite3
from dsa_project.bst import BST, TaskNode
from dsa_project.linked_list import TaskLinkedList
from dsa_project.queue import Task
from dsa_project.Stack import UndoRedoManager, TaskAction

class TaskManager:
    def __init__(self, db_path='dsa_project/tasks.db'):
        self.bst = BST()
        self.task_list = TaskLinkedList()
        self.undo_redo_manager = UndoRedoManager()
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()
        self.load_tasks()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    priority INTEGER NOT NULL
                )
            """)

    def load_tasks(self):
        with self.conn:
            cursor = self.conn.execute("SELECT id, title, priority FROM tasks")
            for row in cursor:
                task = Task(task_id=row[0], title=row[1], priority=row[2])
                self.bst.insert(task)
                self.task_list.insert_at_tail(task)

    def add_task(self, title, priority):
        with self.conn:
            cursor = self.conn.execute("INSERT INTO tasks (title, priority) VALUES (?, ?)", (title, priority))
            task_id = cursor.lastrowid
            task = Task(task_id=task_id, title=title, priority=priority)
            self.bst.insert(task)
            self.task_list.insert_at_tail(task)
            action = TaskAction('CREATE', {'id': task_id, 'title': title, 'priority': priority})
            self.undo_redo_manager.execute_action(action)
            return task

    def delete_task(self, task_id, priority):
        with self.conn:
            cursor = self.conn.execute("SELECT id, title, priority FROM tasks WHERE id = ?", (task_id,))
            task_data = cursor.fetchone()
            if task_data:
                self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
                self.bst.delete(priority)
                self.task_list.delete_task_by_id(task_id)
                action = TaskAction('DELETE', {'id': task_data[0], 'title': task_data[1], 'priority': task_data[2]})
                self.undo_redo_manager.execute_action(action)

    def get_all_tasks_inorder(self):
        return self.bst.inorder_traversal()

    def get_all_tasks_fifo(self):
        return self.queue.items

    def _delete_task_for_undo(self, task_id, priority):
        with self.conn:
            self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            self.bst.delete(priority)
            self.task_list.delete_task_by_id(task_id)

    def _add_task_for_redo(self, title, priority):
        with self.conn:
            cursor = self.conn.execute("INSERT INTO tasks (title, priority) VALUES (?, ?)", (title, priority))
            task_id = cursor.lastrowid
            task = Task(task_id=task_id, title=title, priority=priority)
            self.bst.insert(task)
            self.task_list.insert_at_tail(task)
            return task

    def undo(self):
        action = self.undo_redo_manager.undo()
        if action:
            if action.action_type == 'CREATE':
                task_data = action.task_data
                self._delete_task_for_undo(task_data['id'], task_data['priority'])
            elif action.action_type == 'DELETE':
                task_data = action.task_data
                self._add_task_for_redo(task_data['title'], task_data['priority'])

    def redo(self):
        action = self.undo_redo_manager.redo()
        if action:
            if action.action_type == 'CREATE':
                task_data = action.task_data
                self._add_task_for_redo(task_data['title'], task_data['priority'])
            elif action.action_type == 'DELETE':
                task_data = action.task_data
                self._delete_task_for_undo(task_data['id'], task_data['priority'])
