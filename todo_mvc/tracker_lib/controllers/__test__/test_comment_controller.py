import unittest

from todo_mvc.tracker_lib.controllers.comment import CommentController


class CommentControllerTest(unittest.TestCase):
    def setUp(self):
        self.controller = CommentController()