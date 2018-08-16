import logging
import lib.helpers.errors as errs
import lib.helpers.error_helper as errs_help

from lib.controllers.task import TaskController

logger = logging.getLogger('logger')


class TaskView:
    def __init__(self):
        self.controller = TaskController()

    # def __print_tasks(self, tasks: typing.List[Task]):
    #     pass
    #     # if tasks:
    #     #     for task in tasks:
    #     #         print(task)

    def get_tasks(self, args):
        pass
        # tasks: typing.List[Task] = self.controller.get_tasks()
        # self.__print_tasks(tasks)

    def create_new_task(self, args):
        self.controller.create_task(args.title, args.text, args.status, args.tags, args.parent_title, args.date)

    def create_new_periodic_task(self, args):
        self.controller.create_periodic_task(args.title, args.text, args.status, args.start_date,
                                             args.date, args.period,  args.tags, args.parent_title)

    def get_task_by_title(self, args):
        task = self.controller.get_task_by_title(args.title)
        print(task)

    def delete_task_by_title(self, args):
        try:
            self.controller.delete_task_by_title(args.title)
        except errs.TitleError as e:
            errs_help.console_print(e)
        # try:
        #     task: Task = self.controller.find_task_by_title(args.title)
        #     self.controller.delete_task(task.id, args.date)
        # except errs.TitleError as e:
        #     err_help.console_print(e)
        #     logger.error(e.name)

    def edit_task_title(self, args):
        try:
            self.controller.edit_task_title(args.title, args.new_title)
        except errs.TitleError as e:
            errs_help.console_print(e)
        # try:
        #     task: Task = self.controller.find_task_by_title(args.title)
        #     self.controller.edit_task_title(task.id, args.new_title)
        # except errs.TitleError as e:
        #     err_help.console_print(e)
        #     logger.error(e.name)

    def edit_task_text(self, args):
        try:
            self.controller.edit_task_text(args.title, args.new_text)
        except errs.TitleError as e:
            errs_help.console_print(e)

    def edit_task_status(self, args):
        try:
            self.controller.edit_task_status(args.title, args.new_status)
        except errs.TitleError as e:
            errs_help.console_print(e)
        # try:
        #     task: Task = self.controller.find_task_by_title(args.title)
        #     self.controller.edit_task_status(task.id, args.new_status)
        # except (errs.TitleError, errs.IncorrectValueError) as e:
        #     err_help.console_print(e)
        #     logger.error(e.name)

    def get_tasks_by_tag(self, args):
        task = self.controller.get_task_by_tag(args.tag)
        print(task)
        # tasks: typing.List[Task] = self.controller.get_tasks_by_tag(args.tag)
        # self.__print_tasks(tasks)

    def get_subtasks_of_task(self, args):
        try:
            self.controller.get_subtasks_of_task(args.title)
        except errs.TitleError as e:
            errs_help.console_print(e)

        # try:
        #     task: Task = self.controller.find_task_by_title(args.title)
        #     subtasks: typing.List[Task] = self.controller.get_subtasks_of_task(task.id)
        #     self.__print_tasks(subtasks)
        # except errs.TitleError as e:
        #     err_help.console_print(e)
        #     logger.error(e.name)

    def share_task_permission(self, args):
        try:
            self.controller.share_permission(args.user_login, args.title)
        except errs.TitleError as e:
            errs_help.console_print(e)
        # try:
        #     task: Task = self.controller.find_task_by_title(args.title)
        #     self.controller.share_task_permission(task.id, args.user_login)
        # except(errs.UserNotExistError, errs.TitleError) as e:
        #     err_help.console_print(e)
        #     logger.error(e.name)

    def get_tasks_on_period(self, args):
        pass
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
        #         for task in task_date:
        #             if temp_date.date().__str__() in task_date[task]['dates']:
        #                 is_printable = True
        #                 tasks_to_print[task] = task_date[task]
        #
        #         if is_printable:
        #             print(temp_date.date().__str__() + ':')
        #             print('tasks:')
        #             for task in tasks_to_print:
        #                 print(task)
        #                 for comment in tasks_to_print[task]['dates'][temp_date.date().__str__()]:
        #                     print('comments:')
        #                     print('-' + comment.__str__())
        #
        #         is_printable = False
        #
        #         temp_date = temp_date + timedelta(days=1)
        # except (errs.CronValueError, errs.IncorrectDateValueError, ValueError, TypeError) as e:
        #         err_help.console_print(e)
