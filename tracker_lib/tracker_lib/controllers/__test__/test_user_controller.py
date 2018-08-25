import unittest

from tracker_lib.controllers.task import TaskController


class TaskControllerTest(unittest.TestCase):
    def setUp(self):
        self.controller = TaskController()

