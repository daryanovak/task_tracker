import todo_mvc.tracker_lib.storage.task as task_storage
from todo_mvc.tracker_lib.models import Task, PeriodicTask
import croniter
from datetime import datetime, timedelta
from todo_mvc.tracker_lib.enums import Parameters
from todo_mvc.tracker_lib.enums import Status
import todo_mvc.tracker_lib.helpers.errors as errs
from todo_mvc.tracker_lib.helpers.cron_period_helper import CronPeriodHelper

import logging

logger = logging.getLogger('logger')


class TaskController:
    def __init__(self, user_id):
        self.cph = CronPeriodHelper
        self.user_id = user_id

    def check_if_task_exist(self, task_id, user_id):
        return_value = task_storage.check_task_exist(task_id=task_id, user_id=user_id)

        if return_value == errs.TaskNotExistError().code:
            raise errs.TaskWithParentIdNotExistError()

        if return_value == errs.TaskWithParentIdNotExistError().code:
            logger.error(errs.TaskWithParentIdNotExistError().name)
            raise errs.TaskWithParentIdNotExistError()

        else:
            return True

    def check_if_periodic_task_exist(self, task_id, user_id):
        return_value = task_storage.check_periodic_task_exist(task_id=task_id, user_id=user_id)

        if return_value == errs.TaskNotExistError().code:
            logger.error(errs.TaskNotExistError().name)
            raise errs.TaskWithParentIdNotExistError()

        if return_value == errs.TaskNotExistError().code:
            logger.error(errs.TaskNotExistError().name)
            raise errs.TaskNotExistError()

        else:
            return True

    def create_task(self, title: str, text: str, status: int, tags="", parent_id=None, date=None):
        """
        Creates a new task
        :param title: title of task: str
        :param text: text :str
        :param status: status {0,1,2}
        :param tags: tags:str
        :param parent_id: task id, for which current task will be belong
        :param date: date
        """

        if date:
            date_object = datetime.strptime(date, '%d/%m/%y %H:%M')
        else:
            date_object = None

        if parent_id:
            if self.check_if_task_exist(task_id=parent_id, user_id=self.user_id):
                return task_storage.add_task(user_id=self.user_id, title=title, text=text, status=status, tags=tags,
                                             parent_id=parent_id, date=date_object)
        else:
            parent_id = None
            return task_storage.add_task(user_id=self.user_id, title=title, text=text, status=status, tags=tags,
                                         parent_id=parent_id, date=date_object)

    def create_periodic_task(self, title: str, text: str, status: int, start_date: str, date: str,
                             period: str, tags=None, parent_id=None):
        """
        Creates a perios
        :param title: title
        :param text: text
        :param status: status {0,1,2}
        :param start_date: start date of period
        :param date: end date of period
        :param period: :string cron, witch means a
        :param tags: string of list
        :param parent_id:task id, for which current task will be belong
        :return: created task
        """
        d = datetime.now()

        if CronPeriodHelper.check_croniter(period=period):
            if date:
                date_object = datetime.strptime(date, '%d/%m/%y %H:%M')
            else:
                date_object = None

            if start_date:
                start_date_object = datetime.strptime(start_date, '%d/%m/%y %H:%M')
            else:
                start_date_object = None

            if parent_id:
                if not self.check_if_task_exist(task_id=parent_id, user_id=self.user_id):
                    parent_id = None
            return task_storage.add_periodic_task(user_id=self.user_id, title=title, text=text, status=status,
                                                          start_date=start_date_object, date=date_object, period=period,
                                                          tags=tags,
                                                          parent_id=parent_id)

        else:
            raise errs.CronValueError()

    def get_task_by_id(self, task_id: int):
        """
        Gets task by id
        :param task_id: task id
        :return: task
        """
        if task_storage.check_permission(user_id=self.user_id, task_id=task_id):
            logger.info('Get task by id = %s was found!' % task_id)
            return task_storage.get_task_by_id(task_id=task_id)

        else:
            logger.error(errs.AccessError().name)
            raise errs.AccessError()

    def get_tasks(self):
        """
        Shows all tasks
        :return: All task of authorized user_id
        """
        logger.info('Gets all user tasks!')
        return task_storage.get_tasks(user_id=self.user_id)

    def delete_task(self, task_id: int):
        """
        Deletes task by id
        :param task_id: task id
        """
        if task_storage.check_permission(user_id=self.user_id, task_id=task_id):
            task = task_storage.get_task_by_id(task_id=task_id)

            if task['creator'] == self.user_id:
                task_storage.delete_task(task_id=task_id)
                logger.info('Task, with id = %s was deleted!' % task_id)

            else:
                logger.error(errs.UserNotHaveAccessToTaskError().name)
                raise errs.UserNotHaveAccessToTaskError()

        else:
            logger.error(errs.AccessError().name)
            raise errs.AccessError()

    def edit_task(self, task_id: int, edit_parametr: Parameters, new_parametr_value):
        if task_storage.check_permission(task_id=task_id, user_id=self.user_id):
            return_value = task_storage.edit_task(task_id=task_id, enum_parameter_value=edit_parametr,
                                                  modified_parameter=new_parametr_value)

            if return_value == errs.TaskNotExistError().code:
                logger.error(errs.InvalidTypeParameterError().name)
                raise errs.TaskNotExistError()

            if return_value:
                logger.info('Edit task %s with id = %s. New title = %s!' % (edit_parametr.name, task_id,
                                                                            str(new_parametr_value)))
        else:
            logger.error(errs.TaskNotExistError().name)
            raise errs.TaskNotExistError()

    def edit_task_title(self, task_id: int, new_title: str):
        """
        Changes task by id of authorized user_id
        :param task_id:  tassk id : int
        :param new_title: title : str
        """
        self.edit_task(task_id=task_id, edit_parametr=Parameters.TITLE, new_parametr_value= new_title)

    def edit_task_text(self, task_id: int, new_text: str):
        """
        Changes task text by id
        :param task_id: task id
        :param new_text: new text
        """
        self.edit_task(task_id=task_id, edit_parametr=Parameters.TEXT, new_parametr_value=new_text)

    def edit_task_status(self, task_id: int, new_status):
        """
        Changes task status
        :param task_id: task id
        :param new_status: new status {0,1,2} int
        """
        if new_status.isdigit():
            new_status = int(new_status)
            values = [item.value for item in Status]

            if new_status in values:

                if type(new_status) is int:
                    self.edit_task(task_id=task_id, new_parametr_value=new_status, edit_parametr=Parameters.STATUS)

                else:
                    logger.error(errs.InvalidTypeParameterError().name)
                    raise errs.InvalidTypeParameterError()

            else:
                logger.error(errs.StatusValueError().name)
                raise errs.StatusValueError()

        else:
            logger.error(errs.InvalidTypeParameterError().name)
            raise errs.InvalidTypeParameterError()

    def get_subtasks_of_task(self, task_id: int):
        """
        Gets all subtask of task by her id
        :param task_id: task id
        :return: tasks
        """
        if task_storage.check_permission(task_id=task_id, user_id=self.user_id):
            task_lst = task_storage.get_subtask_of_task(user_id=self.user_id, task_id=task_id)

            if task_lst:
                logger.info('Get subtasks of task with id = %s!' % task_id)
                return task_lst

            else:
                logger.error(errs.NoSubtaskError().name)
                raise errs.NoSubtaskError()
        else:
            logger.error(errs.AccessError().name)
            raise errs.AccessError()

    def share_permission(self, new_user_id: int, task_id: int):
        """
        Share permission to another user_id by his id
        :param new_user_id: user_id id :int
        :param task_id: task id : int
        """
        if task_storage.check_permission(user_id=self.user_id, task_id=task_id):
            task_storage.share_permission(user_id=self.user_id, task_id=task_id, new_user_id=new_user_id)

            logger.info('Share permission to task with id = %s. New user = %s!' % (task_id, new_user_id))

        else:
            logger.error(errs.AccessError().name)
            raise errs.AccessError()

    def get_task_by_tag(self, tag: str):
        """
        Gets task by tags
        :param tag: tag: str
        :return: tasks
        """
        if type(tag) is str:
            return task_storage.get_tasks_by_type_of_parameter(user_id=self.user_id, parameter=Parameters.TAGS, parametr_value=tag)

        else:
            logger.error(errs.InvalidTypeParameterError().name)
            raise errs.InvalidTypeParameterError()

    def get_tasks_on_period(self, start: datetime, end: datetime):
        """
        Gets tasks by date period
        :param start: start of period: datetime in format '%d/%m/%y'
        :param end: end of period : datetime in '%d/%m/%y'
        :return: tasks
        """
        # start = datetime.strptime(start, '%d/%m/%y %H:%M')
        # end = datetime.strptime(end, '%d/%m/%y %H:%M')
        # current_user_id = user_storage.get_current_user()
        cph = CronPeriodHelper()
        start_date = datetime.strptime(start, '%d/%m/%y')
        end_date = datetime.strptime(end, '%d/%m/%y')
        tasks = task_storage.get_tasks(self.user_id)
        task_date_comments_dict = dict()
        response = []

        # if type(start) != datetime or type(end) != datetime:
        # response = {}
        #     raise errs.IncorrectDateValueError()

        # for task in tasks:
        #     if isinstance(task, PeriodicTask):
        #         dates = cph.get_tasks_periods(start_date, end_date,
        #                                       task.period)
        #         dates_dict = dict()
        #         for date in dates:
        #             dates_dict[date] = comment_storage.get_comments_of_task(current_user_id, task.id)
        #         task_date_comments_dict[task] = {'dates': dates_dict}

        temp_date = start_date

        for i in range(int((end_date - start_date).days) + 1):
            tasks_list = list()

            for task in tasks:

                if isinstance(task, PeriodicTask):

                    if cph.in_period(task.period, temp_date):
                        tasks_list.append(task)

                else:

                    if temp_date == task.date:

                        if task.periodic_task_id:
                            tasks_list = list(filter(lambda task: task.id == task.periodic_task_id, tasks_list))
                        tasks_list.append(task)

            if len(tasks_list) > 0:
                response.append({temp_date: tasks_list})

            temp_date = temp_date + timedelta(days=1)

        # temp_date = start_date
        #
        #
        # is_printable = False
        # for i in range(int((end_date - start_date).days) + 1):
        #     tasks_to_print = dict()
        #
        #     for task in task_date_comments_dict:
        #         if temp_date.date().__str__() in task_date_comments_dict[task]['dates']:
        #             is_printable = True
        #             tasks_to_print[task] = task_date_comments_dict[task]
        #
        #     if is_printable:
        #         response[temp_date] = tasks_to_print
        #         # print(temp_date.date().__str__() + ':')
        #         # print('tasks:')
        #         # for task in tasks_to_print:
        #         #     print(task)
        #         #     for comment in tasks_to_print[task]['dates'][temp_date.date().__str__()]:
        #         #         print('comments:')
        #         #         print('-' + comment.__str__())
        #
        #     is_printable = False
        #
        #     temp_date = temp_date + timedelta(days=1)

        return response



