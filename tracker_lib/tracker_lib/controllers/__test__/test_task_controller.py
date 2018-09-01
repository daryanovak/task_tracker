import unittest
import tracker_lib.helpers.errors as errs
from tracker_lib.controllers.task import TaskController
#python3.6 -m unittest discover


class TaskControllerTestCase(unittest.TestCase):
    def setUp(self):
        self.controller = TaskController(user_id=1)

    def test_create_task(self):
        task = {'title': '__test__ title', 'text': '__test__ text', 'status': 1}
        created_task = self.controller.create_task(task['title'], task['text'], task['status'])
        self.assertEqual(task['title'], created_task.title)
        self.assertEqual(task['text'], created_task.text)
        self.assertEqual(task['status'], created_task.status)
        self.controller.delete_task(created_task.id)

    def test_create_periodic_task(self):
        task = {'title': '__test__ title', 'text': '__test__ text', 'status': 1, 'start_date': '31/12/98 00:00',
                'deadline': '31/12/02 00:00', 'period': '* * * * *', 'tags': "test_love"}
        created_task = self.controller.create_periodic_task(title=task['title'],text=task['text'],status=task['status'],
                                                            start_date=task['start_date'], deadline=task['deadline'],
                                                            period=task['period'],tags=task['tags'])
        self.assertEqual(task['title'], created_task.title)
        self.assertEqual(task['text'], created_task.text)
        self.assertEqual(task['status'], created_task.status)
        self.assertEqual(task['period'], created_task.period)

    def test_check_permisson(self):
        with self.assertRaises(errs.TaskNotExistError):
            self.controller.check_permission(user_id=45, task_id=1111)

    def test_get_task_by_id(self):
        task = {'title': '__test__ title', 'text': '__test__ text', 'status': 1}
        created_task = self.controller.create_task(task['title'], task['text'], task['status'])
        task = self.controller.get_task_by_id(task_id=created_task.id)
        self.assertEqual(task['id'], created_task.id)
        self.controller.delete_task(created_task.id)

    def test_edit_title(self):###########3
        task = {'title': '__test__ title', 'text': '__test__ text', 'status': 1}
        created_task = self.controller.create_task(task['title'], task['text'], task['status'])
        task = self.controller.edit_task(created_task.id, {'title': 'NEW'})
        self.assertNotEqual(created_task.title, "NEW")
        self.controller.delete_task(created_task.id)


    def test_edit_text(self):
        task = {'title': '__test__ title', 'text': '__test__ text', 'status': 1}
        created_task = self.controller.create_task(task['title'], task['text'], task['status'])
        task = self.controller.edit_task(created_task.id, {'text': "lol"})
        self.assertNotEqual(created_task.status, "RARA")
        self.controller.delete_task(created_task.id)

    def test_get_subtasks(self):
        task = {'title': '__test__ title', 'text': '__test__ text', 'status': 1}
        created_task = self.controller.create_task(task['title'], task['text'], task['status'])
        subtask = self.controller.create_task(task['title'], task['text'], task['status'], parent_id=created_task.id)
        task_subtasks = self.controller.get_task_subtasks(task_id=created_task.id)
        self.assertIsNotNone(task_subtasks)

    def test_share_permission(self):
        task = {'title': '__11test__ title', 'text': '__test__ text', 'status': 1}
        created_task = self.controller.create_task(task['title'], task['text'], task['status'])
        self.controller.share_permission(task_id=created_task.id, new_user_id=1)
        self.assertEqual([1], created_task.users)

    def test_get_by_tag(self):
        task = {'title': '__11test__ title', 'text': '__test__ text', 'status': 1, 'tag': 'life'}
        created_task = self.controller.create_task(task['title'], task['text'], task['status'], tags=task['tag'])
        tasks = self.controller.get_tasks_by_tag("life")
        self.assertIsNotNone(task)

    def test_task_parameters_type(self):
        task = {'title': '__11test__ title', 'text': '__test__ text', 'status': 1, 'tag': 'life'}
        created_task = self.controller.create_task(task['title'], task['text'], task['status'], tags=task['tag'])
        self.assertIsInstance(created_task.title, str)
        self.assertIsInstance(created_task.text, str)
        self.assertIsInstance(created_task.status, int)
        self.assertIsInstance(created_task.tags, str)
        self.controller.delete_task(created_task.id)

    def test_task_type(self):
        tasks = self.controller.get_tasks()
        self.assertIsInstance(tasks, list)

    def test_cron_string_periodic_task(self):
        with self.assertRaises(errs.CronValueError):
            self.controller.create_periodic_task(title="title", text="text,", status=1, start_date="01/02/12 00:00",
                                                 deadline="02/02/12 00:00", period="* * help", parent_id=666)

    def test_parent_id_periodic_task(self):
        with self.assertRaises(errs.TaskWithParentIdNotExistError):
            self.controller.create_periodic_task(title="title", text="text,", status=1, start_date="01/02/12 00:00", deadline="02/02/12 00:00", period="* * * * *", parent_id=666)

    def test_delete_task(self):
        with self.assertRaises(errs.TaskNotExistError):
            self.controller.delete_task(task_id=89)

    def test_share_permission_exception(self):
        with self.assertRaises(errs.TaskNotExistError):
            self.controller.share_permission(new_user_id=1, task_id=666)










