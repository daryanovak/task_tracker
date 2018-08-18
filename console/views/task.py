import logging
import lib.helpers.errors as errs
import lib.helpers.error_helper as errs_help

from lib.controllers.task import TaskController

logger = logging.getLogger('logger')


class TaskView:
    def __init__(self):
        self.controller = TaskController()

    def get_tasks(self, args):
        pass
        # tasks: typing.List[Task] = self.controller.get_tasks()
        # self.__print_tasks(tasks)

    def create_new_task(self, args):
        self.controller.create_task(args.title, args.text, args.status, args.tags, args.parent_id, args.date)

    def create_new_periodic_task(self, args):
        self.controller.create_periodic_task(args.title, args.text, args.status, args.start_date,
                                             args.date, args.period,  args.tags, args.parent_id)

    def delete_task(self, args):
        try:
            self.controller.delete_task(args.task_id)
        except (errs.AccessError, errs.TitleError) as e:
            errs_help.console_print(e)

    def show_my_tasks(self, args):#проблемы!!!!!!!!!!!!!
        tasks = self.controller.show_my_tasks()
        for task in tasks:
            print(str(task.id) + "--id--" + " " + task.title +" " + task.text + " " + str(task.status))

    def get_task_by_id(self, args):
        try:
            task = self.controller.get_task_by_id(args.task_id)
            print(task)  # напечатать красиво dict
        except (errs.TaskNotExistError,errs.AccessError) as e:
            errs_help.console_print(e)

    def get_task_by_title(self,args):
        tasks = self.controller.get_tasks_by_title(args.title)
        for task in tasks:
            print(str(task.id) + str(task))
            print("___________________")

    def edit_task_title(self, args):
        try:
            self.controller.edit_task_title(args.task_id, args.new_title)
        except (errs.AccessError, errs.TaskNotExistError) as e:
            errs_help.console_print(e)
            logger.error(e.name)

    def edit_task_text(self, args):
        try:
            self.controller.edit_task_text(args.task_id, args.new_text)
        except (errs.TaskNotExistError,errs.AccessError) as e:
            errs_help.console_print(e)
            logger.error(e.name)

    def edit_task_status(self, args):
        try:
            self.controller.edit_task_status(args.task_id, args.new_status)
        except errs.TitleError as e:
            errs_help.console_print(e)
            logger.error(e.name)

    def get_tasks_by_tag(self, args):
        try:
            tasks = self.controller.get_task_by_tag(args.tag)

            for task in tasks:
                print(str(task.id) + "--id--" + " " + task.title +" " + task.text + " " + str(task.status))

        except (errs.TaskNotExistError, errs.TitleError) as e:
            errs_help.console_print(e)
            logger.error(e.name)

    def get_subtasks_of_task(self, args):
        try:
            subtasks = self.controller.get_subtasks_of_task(args.task_id)
            for subtask in subtasks:
                print(str(subtask.id) + "--id--" + " " + subtask.title +" " + subtask.text + " " + str(subtask.status))
        except (errs.TaskNotExistError, errs.TitleError) as e:
            errs_help.console_print(e)
            logger.error(e.name)

    def share_task_permission(self, args):
        try:
            self.controller.share_permission(args.new_user_id, args.task_id)
        except (errs.TaskNotExistError, errs.TitleError, errs.AccessError) as e:
            errs_help.console_print(e)
            logger.error(e.name)

    def get_tasks_on_period(self, args):
        tasks = self.controller.get_tasks_on_period(args.start, args.end)
        for task in tasks:
            print(str(task.id) + "--id--" + " " + task.title + " " + task.text + " " + str(task.status))
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
