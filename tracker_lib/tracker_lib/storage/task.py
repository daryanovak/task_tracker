import _pickle as cPickle
import datetime
import typing

from pony.orm import (
    db_session,
    select,
    delete
)

import tracker_lib.helpers.errors as errs
from tracker_lib.enums import TaskParameters
from tracker_lib.helpers.logging_helper import get_logger
from tracker_lib.models import PeriodicTask
from tracker_lib.models import Task

logger = get_logger()


def __filterByUser(user_id, tasks):
    """
    Returns all user tasks
    :param user_id:
    :param tasks: tasks, which you should check
    :return: list of task object
    """
    tasks_lst = []

    for task in tasks:
        for u in task.users:
            if u == user_id:
                tasks_lst.append(task)
                break
    return tasks_lst


@db_session
def check_permission(user_id: int, task_id: int):
    """
    Check if task with[task_id] belongs to user with [user_id]
    :param user_id:
    :param task_id:
    :return: bool
    """
    task = Task[task_id]
    return user_id in task.users


@db_session
def check_task_exist(task_id: int, user_id: int):
    """
    Checks if simple task with[task_id] belong to user with [user_id]
    :param task_id:
    :param user_id:
    :return: True if exist, else raise exception
    """
    task = Task.get(id=task_id)
    if task:
        if user_id in task.users:
            return True
        else:
            return errs.TaskNotExistError().code
    else:
        return errs.TaskWithParentIdNotExistError().code


@db_session
def check_periodic_task_exist(task_id: int, user_id: int):
    """
    Checks if periodic task with [task_id] belong to user with[user_id]
    :param task_id:
    :param user_id:
    :return:
    """
    task = PeriodicTask.get(id=task_id)

    if task:
        if user_id in task.users:
            return True
        else:
            return errs.TaskWithParentIdNotExistError().code
    else:
        return errs.TaskNotExistError().code


@db_session
def get_task_by_id(task_id: int):
    """
    Gets task from database with such [task_id] and converts it to dict
    :param task_id:
    :param user_id:
    :return: task dict() or raise
    """
    task = Task.get(id=task_id)
    return task.to_dict()


@db_session
def add_task(user_id: int, title: str, text: str, status: int, tags: str, date=None, parent_id=None,
             periodic_task_id=None):
    """
     Adds simple task to database.
    :param user_id:
    :param title:
    :param text:
    :param status:
    :param tags:
    :param date: optional
    :param parent_id: optional
    :param periodic_task_id:
    :return: task
    """

    users = [user_id]
    if parent_id:
        parent_task = get_task_by_id(parent_id)
        users = parent_task['users']

    task = Task(creator=user_id, title=title, text=text, status=status, tags=tags,
                date=date, parent_id=parent_id, periodic_task_id=periodic_task_id, users=users)

    return task


@db_session
def add_periodic_task(user_id: int, title: str, text: str, status: int, tags: str, start_date: datetime, period: str,
                      deadline=None, parent_id=None):
    users = [user_id]
    if parent_id:
        parent_task = get_task_by_id(parent_id)
        users = parent_task['users']

    periodic_task = PeriodicTask(creator=user_id, title=title, text=text, status=status, tags=tags, start_date=start_date,
                                 period=period, date=deadline, parent_id=parent_id, users=users)

    return periodic_task


@db_session
def delete_task(task_id: int):
    task = Task[task_id]

    delete(p for p in Task if p.parent_id == task_id)
    task.delete()


@db_session
def edit_task(task_id: int, edited_task: typing.Dict):
    task = Task[task_id]
    if task:
        task.set(**edited_task)
    else:
        return errs.TaskNotExistError().code


@db_session
def edit_periodic_task(task_id: int, edited_task: typing.Dict):
    task = PeriodicTask[task_id]
    if task:
        task.set(**edited_task)
    else:
        return errs.TaskNotExistError().code


@db_session
def get_task_subtasks(user_id: int, task_id: int):
    tasks = select(t for t in Task
                   if t.parent_id == task_id).prefetch(Task.title)
    tasks = __filterByUser(user_id, tasks)

    lst = [task.to_dict() for task in tasks]

    for task in lst:
        task['subtasks'] = get_task_subtasks(user_id, task['id'])

    return lst


@db_session
def share_permission(user_id: int, task_id: int, new_user_id: int, parent_id: int=None):

    if parent_id:
        tasks = select(t for t in Task
                       if t.parent_id == parent_id).prefetch(Task)

        tasks = __filterByUser(user_id, tasks)
        for task in tasks:
            task.users.append(int(new_user_id))
            share_permission(user_id, task_id, new_user_id, task.id)
    else:
        task = Task[task_id]
        task.users.append(int(new_user_id))

        tasks = select(t for t in Task
                       if t.parent_id == task_id).prefetch(Task)
        tasks = __filterByUser(user_id, tasks)

        if len(tasks):
            for _task in tasks:
                share_permission(user_id, _task.id, new_user_id, task.id)


@db_session
def delete_permission(task_id: int, deleted_user_id: int):
    task = Task[task_id]
    users = []
    for user_id in task.users:
        if user_id != deleted_user_id:
            users.append(user_id)

    task.users = users


@db_session
def get_tasks_on_period(user_id: int, start: datetime, end: datetime):
    tasks = select(t for t in Task
                   for user in t.users if user.id == user_id).prefetch(Task.title)
    pickled_data = cPickle.dumps(tasks)
    tasks = cPickle.loads(pickled_data)

    return_list = []

    for task in tasks:
        if type(task) is PeriodicTask:
            if end >= task.date and start <= task.start_date:
                return_list.append(task)

        if type(task) is Task:
            if end >= task.date >= start:
                return_list.append(task)

    return return_list


@db_session
def get_tasks_by_parameter_type(user_id: int, parameter: TaskParameters, parametr_value):
    if parameter == TaskParameters.TITLE:
        tasks = select(t for t in Task
                       if user_id in t.users
                       if t.title == parametr_value).prefetch(Task.title)
        pickled_data = cPickle.dumps(tasks)
        tasks = cPickle.loads(pickled_data)

    if parameter == TaskParameters.TEXT:
        return Task.get(text=parametr_value)

    if parameter == TaskParameters.STATUS:
        return Task.get(status=parametr_value)

    if parameter == TaskParameters.TAGS:
        tasks = select(t for t in Task).prefetch(Task.title)
        _tasks = []
        for task in tasks:
            if user_id in task.users:
                _tasks.append(task)

        pickled_data = cPickle.dumps(_tasks)
        tasks = cPickle.loads(pickled_data)

        lst = []

        for task in tasks:
            if task.tags != "":
                list_of_tags = map(lambda tag: tag.strip(), task.tags.split(","))
                if parametr_value in list_of_tags:
                    lst.append(task.to_dict())
        return lst


@db_session
def get_tasks(user_id: int):
    tasks = (select(task for task in Task if task.parent_id is None).prefetch(Task))

    tasks_lst = []

    for task in tasks:
        if isinstance(task, Task) and not isinstance(task, PeriodicTask):
            for u in task.users:
                if u == user_id:
                    tasks_lst.append({'id': task.id, 'classtype': "Task", 'title': task.title, 'text': task.text,
                                      'status': task.status, 'tags': task.tags, 'date': task.date,
                                      'parent_id': task.parent_id, 'creator': task.creator, 'periodic_task_id': task.periodic_task_id})

        if isinstance(task, PeriodicTask):
            for u in task.users:
                if u == user_id:
                    tasks_lst.append({'id': task.id, 'classtype': "PeriodicTask", 'title': task.title, 'text': task.text,
                                      'status': task.status, 'tags': task.tags, 'start_date': task.start_date,
                                      'period': task.period, 'date': task.date, 'parent_id': task.parent_id,
                                      'creator': task.creator})
    for task in tasks_lst:
        task['subtasks'] = get_task_subtasks(user_id, task['id'])
    return tasks_lst
