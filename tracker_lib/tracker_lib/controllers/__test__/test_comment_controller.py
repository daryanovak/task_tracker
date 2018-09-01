import unittest

from tracker_lib.controllers.comment import CommentController
from tracker_lib.controllers.task import TaskController
import tracker_lib.helpers.errors as errs


class CommentControllerTest(unittest.TestCase):
    def setUp(self):
        self.controller = CommentController(user_id=1)
        self.task_controller = TaskController(user_id=1)

    def test_get_comment(self):
        task = {'title': '__test__ title', 'text': '__test__ text', 'status': 1}
        created_task = self.task_controller.create_task(task['title'], task['text'], task['status'])
        self.controller.create_task_comment(task_id=created_task.id, text="TEXT")
        comments = self.controller.get_task_comments(task_id=created_task.id)
        self.assertIn("TEXT", comments[0]['text'])
        self.task_controller.delete_task(created_task.id)

    def test_create_comment(self):
        task = {'title': '__test__ title', 'text': '__test__ text', 'status': 1}
        created_task = self.task_controller.create_task(task['title'], task['text'], task['status'])
        comment = self.controller.create_task_comment(task_id=created_task.id, text="lala")
        comments = self.controller.get_task_comments(task_id=created_task.id)
        self.assertIsInstance(comments, list)
        self.task_controller.delete_task(created_task.id)

    def test_check_user_commentw(self):
        with self.assertRaises(errs.CommentNotFoundError):
            self.controller.check_user_in_comment(user_id=1, comment_id=1777)