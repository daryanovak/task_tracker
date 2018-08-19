import unittest

from lib.controllers.task import TaskController


class TaskControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.controller = TaskController()

    def test_create_task(self):
        task = { 'title': '__test__ title', 'text': '__test__ text', 'status': 1 }
        created_task = self.controller.create_task(task['title'], task['text'], task['status'])
        self.assertEqual(task['title'], created_task.title)
        self.assertEqual(task['text'], created_task.text)
        self.assertEqual(task['status'], created_task.status)
        self.controller.delete_task(created_task.id)


