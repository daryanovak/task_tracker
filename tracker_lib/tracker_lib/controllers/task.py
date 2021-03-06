"""
This module allows you to perform basic commands with a task.
Also it is required to separate the logic of work with information from the console and django part.
The module requires an already authorized user.

"""
import typing
from datetime import (
    datetime,
    timedelta
)
from enum import Enum

from pony.orm import ObjectNotFound

import tracker_lib.helpers.errors as errs
import tracker_lib.storage.task as task_storage
from tracker_lib.helpers.cron_period_helper import CronPeriodHelper
from tracker_lib.helpers.logging_helper import get_logger


class TaskParameters(Enum):
    TITLE = 1
    TEXT = 2
    STATUS = 3
    TAGS = 4
    PARENT_ID = 5


class TaskStatus(Enum):
    PLANNED = 0
    COMPLETED = 1
    FAILED = 2


logger = get_logger()


class TaskController:
    """

    Class TaskControllers takes current user id for work with user.
    And CronPeriodHelper for works periodic tasks.

    """
    def __init__(self, user_id):
        self.period_helper = CronPeriodHelper
        self.user_id = user_id
        self.__update_status()

    def __update_status(self):
        """
        Updates task status, when deadline is over
        """
        tasks = task_storage.get_tasks(self.user_id)

        for task in tasks:
            if task['date'] and task['date'] < datetime.now():
                task_storage.edit_task(task['id'], {'status': TaskStatus.FAILED.value})

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

    def check_task_exist(self, task_id, user_id):
        """

        Checks if simple_task exist in current user with user_id.

        :param task_id:
        :param user_id:
        :return: True or raise exception
        """
        return_value = task_storage.check_task_exist(task_id=task_id, user_id=user_id)

        if return_value == errs.TaskNotExistError().code:
            raise errs.TaskNotExistError()

        if return_value == errs.TaskWithParentIdNotExistError().code:
            logger.error(errs.TaskWithParentIdNotExistError().name)
            raise errs.TaskWithParentIdNotExistError()

        else:
            return True

    def check_periodic_task_exist(self, task_id, user_id):
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
            if self.check_task_exist(task_id=parent_id, user_id=self.user_id):
                return task_storage.add_task(user_id=self.user_id, title=title, text=text, status=status, tags=tags,
                                             parent_id=parent_id, date=date_object)
        else:
            parent_id = None
            return task_storage.add_task(user_id=self.user_id, title=title, text=text, status=status, tags=tags,
                                         parent_id=parent_id, date=date_object)

    def create_periodic_task(self, title: str, text: str, status: int, start_date: str, deadline: str,
                             period: str, tags=None, parent_id=None):
        """

        Creates a periodic task for user with user_id.

        :param title: title
        :param text: text
        :param status: status {0,1,2}
        :param start_date: start date of period
        :param deadline: end date of period
        :param period: :string cron, which means in which days task will be repeat
        :param tags: string of tags
        :param parent_id: task id, for which current task will be belong
        :return: created periodic task
        """
        if not CronPeriodHelper.is_valid_cron(period=period):
            raise errs.CronValueError()

        if deadline:
            date_object = datetime.strptime(deadline, '%d/%m/%y %H:%M')
        else:
            date_object = None

        if start_date:
            start_date_object = datetime.strptime(start_date, '%d/%m/%y %H:%M')
        else:
            start_date_object = None

        if parent_id:
            if not self.check_task_exist(task_id=parent_id, user_id=self.user_id):
                parent_id = None

        return task_storage.add_periodic_task(user_id=self.user_id, title=title, text=text, status=status,
                                              start_date=start_date_object, deadline=date_object, period=period,
                                              tags=tags, parent_id=parent_id)

    def get_task_by_id(self, task_id: int):
        """

        Gets task by his task_id.
        Checks permission for user to the task and returns.

        :param task_id: task id
        :return: task object converted to dict
        """
        if not self.check_permission(user_id=self.user_id, task_id=task_id):
            logger.error(errs.AccessError().name)
            raise errs.AccessError()

        logger.info('Get task by id = %s was found!' % task_id)

        return task_storage.get_task_by_id(task_id=task_id)

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
        if not self.check_permission(user_id=self.user_id, task_id=task_id):
            logger.error(errs.AccessError().name)
            raise errs.AccessError()

        task = task_storage.get_task_by_id(task_id=task_id)

        if task['creator'] == self.user_id:
            task_storage.delete_task(task_id=task_id)

            logger.info('Task, with id = %s was deleted!' % task_id)

        else:
            logger.error(errs.UserNotHaveAccessToTaskError().name)
            raise errs.UserNotHaveAccessToTaskError()

    def edit_task(self, task_id: int, edited_task: typing.Dict):
        """

        Function which allows you edit the task parameters such title, text, date, period etc.

        :param task_id: task id
        :param edited_task: contains parameters of edited task.
        """
        if not self.check_permission(task_id=task_id, user_id=self.user_id):
            logger.error(errs.TaskNotExistError().name)
            raise errs.TaskNotExistError()

        task = task_storage.get_task_by_id(task_id=task_id)

        if 'date' in edited_task:
            try:
                date = datetime.strptime(edited_task['date'], '%d/%m/%y %H:%M')
                edited_task['date'] = date
            except ValueError:
                raise errs.IncorrectDateValueError()

        values = [str(item.value) for item in TaskStatus]

        if 'status' in edited_task and edited_task['status'] not in values:
            raise errs.StatusValueError()

        if not task['classtype'] == "PeriodicTask":
            return_value = task_storage.edit_task(task_id=task_id, edited_task=edited_task)
            if return_value == errs.TaskNotExistError().code:
                raise errs.TaskNotExistError()

        if 'period' in edited_task and not self.period_helper.is_valid_cron(edited_task['period']):
            raise errs.CronValueError()

        if 'start_date' in edited_task:
            try:
                date = datetime.strptime(edited_task['start_date'], '%d/%m/%y %H:%M')
                edited_task['date'] = date
            except ValueError:
                raise errs.IncorrectDateValueError()

        return_value = task_storage.edit_periodic_task(task_id=task_id, edited_task=edited_task)

        if return_value == errs.TaskNotExistError().code:
            raise errs.TaskNotExistError()


    def get_task_subtasks(self, task_id: int):
        """

        Gets recurrently all subtask of task by her id.

        :param task_id: task id
        :return: all subtasks of task
        """
        if not self.check_permission(task_id=task_id, user_id=self.user_id):
            logger.error(errs.AccessError().name)
            raise errs.AccessError()

        return_value = task_storage.get_task_subtasks(user_id=self.user_id, task_id=task_id)

        if return_value:
            logger.info('Get subtasks of task with id = %s!' % task_id)
            return return_value

    def share_permission(self, new_user_id: int, task_id: int):
        """

        Share permission to another user_id by his id.
        Share permission for the task and her all subtasks.
        Even if subtasks will be added to task later than access to task will be received.

        :param new_user_id: user_id id :int
        :param task_id: task id : int
        """
        if not self.check_permission(user_id=self.user_id, task_id=task_id):
            logger.error(errs.AccessError().name)
            raise errs.AccessError()

        task_storage.share_permission(user_id=self.user_id, task_id=task_id, new_user_id=new_user_id)

        logger.info('Share permission to task with id = %s. New user = %s!' % (task_id, new_user_id))

    def delete_permission(self, task_id, deleted_user_id):
        """

        Deletes access to the task with task id.

        """
        task = self.get_task_by_id(task_id=task_id)
        if task['creator'] == self.user_id or self.user_id in task['users']:
            task_storage.delete_permission(deleted_user_id=deleted_user_id, task_id=task_id)
        else:
            raise errs.AccessError()

    def get_tasks_by_tag(self, tag: str):
        """

        Gets all tasks which have input tag.

        :param tag:
        :return: list of task object
        """
        if not isinstance(tag, str):
            logger.error(errs.InvalidTypeParameterError().name)
            raise errs.InvalidTypeParameterError()

        return task_storage.get_tasks_by_parameter_type(user_id=self.user_id, parameter=TaskParameters.TAGS, parametr_value=tag)

    def get_tasks_on_period(self, start: str, end: str):
        """

        Gets all tasks in predetermined period.

        :param start: start of period, datetime in format '%d/%m/%y'
        :param end: end of period, datetime in '%d/%m/%y'
        :return: tasks
        """
        period_helper = CronPeriodHelper()
        start_date = datetime.strptime(start, '%d/%m/%y')
        end_date = datetime.strptime(end, '%d/%m/%y')

        tasks = task_storage.get_tasks(self.user_id)
        response = []

        temp_date = start_date

        for i in range(int((end_date - start_date).days) + 1):
            tasks_list = []

            for task in tasks:
                if task['classtype'] == 'PeriodicTask':
                    if period_helper.in_period(task['period'], temp_date):
                        tasks_list.append(task)
                else:
                    task_date = task['date']
                    if task_date and temp_date == datetime(task_date.year, task_date.month, task_date.day):

                        if task['periodic_task_id']:
                            tasks_list = list(filter(lambda task: task['id'] == task['periodic_task_id'], tasks_list))
                        tasks_list.append(task)

            if len(tasks_list):
                response.append({temp_date: tasks_list})

            # [ {'12:12:2018': [{name: '123' ..}, ]
            #
            temp_date = temp_date + timedelta(days=1)

        return response



