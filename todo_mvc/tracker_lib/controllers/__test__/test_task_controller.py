import unittest
import todo_mvc.tracker_lib.helpers.errors as errs
from todo_mvc.tracker_lib.controllers.task import TaskController

#python3.6 -m unittest discover
#отдельная база для тестов
#unit test
#либа
#многоуровневое логирование
#help
#документация
#Если раздаем доступ к таске, должен раздаться доступ к подтаскам всем++++++===
#логи???
#bootstrap
#django
#html
#css
#User_id должен передаваться везде, а не только в контроллере


class TaskControllerTestCase(unittest.TestCase):
    def setUp(self):
        #self.controller = TaskController()

    def test_create_task(self):
        task = {'title': '__test__ title', 'text': '__test__ text', 'status': 1}
        created_task = self.controller.create_task(task['title'], task['text'], task['status'])
        self.assertEqual(task['title'], created_task.title)
        self.assertEqual(task['text'], created_task.text)
        self.assertEqual(task['status'], created_task.status)
        self.controller.delete_task(created_task.id)

    def test_cron_periodic_task(self):
        with self.assertRaises(errs.TaskNotExistError):
            TaskController.create_periodic_task(TaskController(), user_id=1, title="title", text="text", status=1,
                                                start_date="01/02/12 00:00", date="02/02/12 00:00", period="* * * * *",
                                                parent_id=666)

    def test_cron_string_periodic_task(self):
        with self.assertRaises(errs.CronValueError):
            TaskController.create_periodic_task(TaskController(), user_id=1,  title="title", text="text,", status=1,
                                                start_date="01/02/12 00:00", date="02/02/12 00:00", period="* * help",
                                                parent_id=666)

    def test_parent_id_periodic_task(self):
        with self.assertRaises(errs.TaskNotExistError):
            TaskController.create_periodic_task(TaskController(),user_id=1,  title="title", text="text,", status=1,
                                                start_date="01/02/12 00:00", date="02/02/12 00:00", period="* * * * *",
                                                parent_id=666)

    def test_delete_task(self):
        with self.assertRaises(errs.TaskNotExistError):
            TaskController.delete_task(TaskController(), user_id=1, task_id=89)

    def test_delete_task(self):
        with self.assertRaises(errs.UserNotHaveAccessToTask):
            TaskController.delete_task(user_id=1, task_id=2)









