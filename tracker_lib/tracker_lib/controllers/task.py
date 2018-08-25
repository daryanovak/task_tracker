"""
This module allows you to perform basic commands with a task.
Also it is required to separate the logic of work with information from the console and django part.
The module requires an already authorized user.

"""
import tracker_lib.storage.task as task_storage
from tracker_lib.models import Task, PeriodicTask
import croniter
from datetime import datetime, timedelta
from tracker_lib.enums import Parameters
from tracker_lib.enums import Status
import tracker_lib.helpers.errors as errs
from tracker_lib.helpers.cron_period_helper import CronPeriodHelper

import logging
from pony.orm import *
logger = logging.getLogger('logger')


class TaskController:
    """

    Class TaskControllers takes current user id for work with user.
    And CronPeriodHelper for works periodic tasks.

    """
    def __init__(self, user_id):
        self.cph = CronPeriodHelper
        self.user_id = user_id

    def check_permission(self, user_id, task_id):
        """

        Checks if user with user_id have permission to task with task_id.

        :param user_id: unique user_id
        :param task_id: unique task_id
        :return: bool type. True if user have access, else raise exception
        """
        try:
            return task_storage.check_permission(user_id=user_id, task_id=task_id)
        except ObjectNotFound:
            logger.error(errs.TaskNotExistError().name)
            raise errs.TaskNotExistError()

    def check_if_task_exist(self, task_id, user_id):
        """

        Checks if simple_task exist in current user with user_id.

        :param task_id:
        :param user_id:
        :return: True or raise exception
        """
        return_value = task_storage.check_task_exist(task_id=task_id, user_id=user_id)

        if return_value == errs.TaskNotExistError().code:
            raise errs.TaskWithParentIdNotExistError()

        if return_value == errs.TaskWithParentIdNotExistError().code:
            logger.error(errs.TaskWithParentIdNotExistError().name)
            raise errs.TaskWithParentIdNotExistError()

        else:
            return True

    def check_if_periodic_task_exist(self, task_id, user_id):
        """

        Checks if periodic task exist in current user

        :param task_id:
        :param user_id:
        :return: return True or raise exception
        """
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

        Creates a new task for user with user_id.

        :param title: title of task: str
        :param text: text :str
        :param status: status {0,1,2}
        :param tags: tags:str of tags
        :param parent_id: task id, for which current task will be belong
        :param date: date of the task event. input string converts to datetime or raise exception
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

        Creates a periodic task for user with user_id.

        :param title: title
        :param text: text
        :param status: status {0,1,2}
        :param start_date: start date of period
        :param date: end date of period
        :param period: :string cron, which means in which days task will be repeat
        :param tags: string of tags
        :param parent_id: task id, for which current task will be belong
        :return: created periodic task
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

        Gets task by his task_id.
        Checks permission for user to the task and returns.

        :param task_id: task id
        :return: task object converted to dict
        """
        if self.check_permission(user_id=self.user_id, task_id=task_id):
            logger.info('Get task by id = %s was found!' % task_id)
            return task_storage.get_task_by_id(task_id=task_id)

        else:
            logger.error(errs.AccessError().name)
            raise errs.AccessError()

    def get_tasks(self):
        """

        Returns all user tasks.

        :return: list of task-dict
        """
        logger.info('Gets all user tasks!')
        return task_storage.get_tasks(user_id=self.user_id)

    def delete_task(self, task_id: int):
        """

        Deletes task by id.
        Check if user have access and then deletes task with her all subtasks.

        :param task_id: task id
        """
        if self.check_permission(user_id=self.user_id, task_id=task_id):
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

    def edit_task(self, task_id: int, edit_parameter: Parameters, new_parametr_value):
        """

        Function which allows you edit the task parameters.

        :param task_id: task id
        :param edit_parameter: enum Parameters, which allows select type of changeable parameter
        :param new_parametr_value:_value: new value of changeable parameter, should be correct type.
        """
        if self.check_permission(task_id=task_id, user_id=self.user_id):
            return_value = task_storage.edit_task(task_id=task_id, enum_parameter_value=edit_parameter,
                                                  modified_parameter=new_parametr_value)

            if return_value == errs.TaskNotExistError().code:
                logger.error(errs.InvalidTypeParameterError().name)
                raise errs.TaskNotExistError()

            if return_value:
                logger.info('Edit task %s with id = %s. New title = %s!' % (edit_parameter.name, task_id,
                                                                            str(new_parametr_value)))
        else:
            logger.error(errs.TaskNotExistError().name)
            raise errs.TaskNotExistError()

    def edit_task_title(self, task_id: int, new_title: str):
        """

        Changes a task title by task id

        :param task_id:  task id : int
        :param new_title: title : str
        """
        self.edit_task(task_id=task_id, edit_parameter=Parameters.TITLE, new_parametr_value= new_title)

    def edit_task_text(self, task_id: int, new_text: str):
        """

        Changes a task text by task id

        :param task_id: task id
        :param new_text: new text
        """
        self.edit_task(task_id=task_id, edit_parameter=Parameters.TEXT, new_parametr_value=new_text)

    def edit_task_status(self, task_id: int, new_status):
        """

        Changes a task status by task id

        :param task_id: task id
        :param new_status: new status {0,1,2} int
        """
        if new_status.isdigit():
            new_status = int(new_status)
            values = [item.value for item in Status]

            if new_status in values:

                if type(new_status) is int:
                    self.edit_task(task_id=task_id, new_parametr_value=new_status, edit_parameter=Parameters.STATUS)

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

        Gets recurrently all subtask of task by her id.

        :param task_id: task id
        :return: all subtasks of task
        """
        if self.check_permission(task_id=task_id, user_id=self.user_id):
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

        Share permission to another user_id by his id.
        Share permission for the task and her all subtasks.
        Even if subtasks will be added to task later than access to task will be received.

        :param new_user_id: user_id id :int
        :param task_id: task id : int
        """
        if self.check_permission(user_id=self.user_id, task_id=task_id):
            task_storage.share_permission(user_id=self.user_id, task_id=task_id, new_user_id=new_user_id)

            logger.info('Share permission to task with id = %s. New user = %s!' % (task_id, new_user_id))

        else:
            logger.error(errs.AccessError().name)
            raise errs.AccessError()

    def get_task_by_tag(self, tag: str):
        """

        Gets all tasks which have input tag.

        :param tag:
        :return: list of task object
        """
        if type(tag) is str:
            return task_storage.get_tasks_by_type_of_parameter(user_id=self.user_id, parameter=Parameters.TAGS, parametr_value=tag)

        else:
            logger.error(errs.InvalidTypeParameterError().name)
            raise errs.InvalidTypeParameterError()

    def get_tasks_on_period(self, start: datetime, end: datetime):
        """

        Gets all tasks in predetermined period.

        :param start: start of period, datetime in format '%d/%m/%y'
        :param end: end of period, datetime in '%d/%m/%y'
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



