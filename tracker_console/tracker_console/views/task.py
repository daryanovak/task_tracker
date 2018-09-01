import tracker_lib.helpers.error_helper as errs_help
import tracker_lib.helpers.errors as errs
from tracker_lib.helpers.logging_helper import get_logger
from tracker_lib.controllers.task import TaskController

from tracker_console.auth.user_controller import UserController
from tracker_console.helpers import get_token
import tracker_console.task_helper as task_helper

logger = get_logger()


class TaskView:
    def __init__(self):
        self.user_controller = UserController()
        self.controller = TaskController(self.user_controller.user_id(get_token()))

    def create_new_task(self, args):
        try:
            self.controller.create_task(args.title, args.text, args.status, args.tags, args.parent_id, args.date)
        except (errs.TaskNotExistError, errs.TaskWithParentIdNotExistError) as e:
            errs_help.console_print(e)
        except ValueError:
            print("Not valid date")

    def create_new_periodic_task(self, args):
        try:
            self.controller.create_periodic_task(args.title, args.text, args.status, args.start_date,
                                                 args.date, args.period,  args.tags, args.parent_id)
        except (errs.TaskWithParentIdNotExistError, errs.TaskNotExistError, errs.CronValueError) as e:
            errs_help.console_print(e)
        # except ValueError:
        #     print("Not valid date")

    def delete_task(self, args):
        try:
            self.controller.delete_task(args.task_id)
        except (errs.AccessError, errs.TitleError, errs.TaskNotExistError, errs.UserNotHaveAccessToTaskError) as e:
            errs_help.console_print(e)

    def get_tasks(self, args):
        tasks = self.controller.get_tasks()
        for task in tasks:
            task_helper.print_task(task)
            self.__print_subtasks(task['subtasks'], 2)

    def get_task_by_id(self, args):
        try:
            task = self.controller.get_task_by_id(args.task_id)
            task_helper.print_task(task)
        except (errs.TaskNotExistError, errs.AccessError) as e:
            errs_help.console_print(e)

    def edit_task(self, args):
        try:
            self.controller.edit_task(args.task_id, {args.parameter: args.new_parameter})
        except (errs.AccessError, errs.CronValueError, errs.TaskNotExistError, errs.StatusValueError,
                errs.IncorrectDateValueError) as e:
            errs_help.console_print(e)

    def get_tasks_by_tag(self, args):
        try:
            tasks = self.controller.get_tasks_by_tag(args.tag)

            for task in tasks:
                # print(str(task.id) + "--id--" + " " + task.title +" " + task.text + " " + str(task.status))
                task_helper.print_task(task)
        except (errs.TaskNotExistError, errs.TitleError) as e:
            errs_help.console_print(e)

    def __print_subtasks(self, subtasks, offset = 0):
        for subtask in subtasks:
            task_helper.print_task(subtask, offset)
            self.__print_subtasks(subtask['subtasks'], offset + 2)

    def get_task_subtasks(self, args):
        try:
            subtasks = self.controller.get_task_subtasks(args.task_id)
            self.__print_subtasks(subtasks)

        except (errs.TaskNotExistError, errs.AccessError, errs.NoSubtaskError) as e:
            errs_help.console_print(e)

    def share_task_permission(self, args):
        try:
            self.controller.share_permission(args.new_user_id, args.task_id)
        except (errs.TaskNotExistError, errs.TitleError, errs.AccessError) as e:
            errs_help.console_print(e)

    def get_tasks_on_period(self, args):
        dates_tasks = self.controller.get_tasks_on_period(args.start, args.end)
        for date_tasks in dates_tasks:
            date = list(date_tasks.keys())[0]
            print(date)
            for task in date_tasks[date]:
                task_helper.print_task(task)

        # for task in tasks:
        #     print(str(task.id) + "--id--" + " " + task.title + " " + task.text + " " + str(task.status))
        # try:
        #     response = self.controller.get_tasks_on_period(args.start, args.end)
        #     task_date = response.get('task_date_comments_dict')
        #     start_date = response.get('start_date')
        #     end_date = response.get('end_date')
        #
        #     temp_date = start_date
        #
        #     is_printable = False
        #     for i in range(int((end_date - start_date).days) + 1):
        #         tasks_to_print = dict()
        #
        #         for tasks in task_date:
        #             if temp_date.date().__str__() in task_date[tasks]['dates']:
        #                 is_printable = True
        #                 tasks_to_print[tasks] = task_date[tasks]
        #
        #         if is_printable:
        #             print(temp_date.date().__str__() + ':')
        #             print('tasks:')
        #             for tasks in tasks_to_print:
        #                 print(tasks)
        #                 for comment in tasks_to_print[tasks]['dates'][temp_date.date().__str__()]:
        #                     print('comments:')
        #                     print('-' + comment.__str__())
        #
        #         is_printable = False
        #
        #         temp_date = temp_date + timedelta(days=1)
        # except (errs.CronValueError, errs.IncorrectDateValueError, ValueError, TypeError) as e:
        #         err_help.console_print(e)
