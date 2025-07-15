import unittest
import os
from dsa_project.task_manager import TaskManager
from dsa_project.queue import Task

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.db_path = 'dsa_project/test_tasks.db'
        self.task_manager = TaskManager(db_path=self.db_path)

    def tearDown(self):
        os.remove(self.db_path)

    def test_add_task(self):
        task = self.task_manager.add_task("Test Task", 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.priority, 1)
        tasks = self.task_manager.get_all_tasks_inorder()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Test Task")

    def test_delete_task(self):
        task = self.task_manager.add_task("Test Task", 1)
        self.task_manager.delete_task(task.task_id, task.priority)
        tasks = self.task_manager.get_all_tasks_inorder()
        self.assertEqual(len(tasks), 0)

    def test_undo_redo_add(self):
        self.task_manager.add_task("Test Task", 1)
        self.task_manager.undo()
        tasks = self.task_manager.get_all_tasks_inorder()
        self.assertEqual(len(tasks), 0)
        self.task_manager.redo()
        tasks = self.task_manager.get_all_tasks_inorder()
        self.assertEqual(len(tasks), 1)

    def test_undo_redo_delete(self):
        task = self.task_manager.add_task("Test Task", 1)
        self.task_manager.delete_task(task.task_id, task.priority)
        self.task_manager.undo()
        tasks = self.task_manager.get_all_tasks_inorder()
        self.assertEqual(len(tasks), 1)
        self.task_manager.redo()
        tasks = self.task_manager.get_all_tasks_inorder()
        self.assertEqual(len(tasks), 0)

if __name__ == '__main__':
    unittest.main()
