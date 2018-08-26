import _pickle as cPickle
import datetime
import logging
import typing

from pony.orm import *

import tracker_lib.helpers.errors as errs
from tracker_lib.enums import Parameters
from tracker_lib.models import PeriodicTask
from tracker_lib.models import Task

logger = logging.getLogger('logger')


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

    logger.info('Task, with id = %s was created!' % task.id)

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

    logger.info('Periodic Task, with id = %s was created!' % periodic_task.id)

    return periodic_task

#
# @db_session
# def get_tasks(user_id: int):
#     tasks = select(t for t in Task
#                    if user_id in t.users).prefetch(Task.title)
#     pickled_data = cPickle.dumps(tasks)
#     tasks = cPickle.loads(pickled_data)
#
#     lst = []
#     for task in tasks:
#         lst.append(task)
#
#     return lst


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
def get_task_subtasks(user_id: int, task_id: int):
    tasks = select(t for t in Task
                  if user_id in t.users
                  if t.parent_id == task_id).prefetch(Task.title)
    pickled_data = cPickle.dumps(tasks)
    tasks = cPickle.loads(pickled_data)

    lst = [task for task in tasks]

    # lst = []
    # for task in tasks:
    #     lst.append(task)

    return lst


@db_session
def share_permission(user_id: int, task_id: int, new_user_id: int, parent_id: int=None):

    if parent_id:
        tasks = select(t for t in Task
                       if user_id in t.users
                       if t.parent_id == parent_id).prefetch(Task)

        for task in tasks:
            task.users.append(int(new_user_id))
            share_permission(user_id, task_id, new_user_id, task.id)
    else:
        task = Task[task_id]
        task.users.append(int(new_user_id))


        tasks = select(t for t in Task
                       if user_id in t.users
                       if t.parent_id == task_id).prefetch(Task)

        if len(tasks):
            for _task in tasks:
                share_permission(user_id, _task.id, new_user_id, task.id)

    # periodic_tasks = select(t for t in PeriodicTask
    #                         if user_id in t.users
    #                         if t.parent_id == task_id).prefetch(Task)
    #
    # for periodic_task in periodic_tasks:
    #     periodic_task.users.append(new_user_id)



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
def get_tasks_by_parameter_type(user_id: int, parameter: Parameters, parametr_value):
    if parameter == Parameters.TITLE:
            tasks = select(t for t in Task
                           if user_id in t.users
                           if t.title == parametr_value)
            pickled_data = cPickle.dumps(tasks)
            tasks = cPickle.loads(pickled_data)

    if parameter == Parameters.TEXT:
            return Task.get(text=parametr_value)

    if parameter == Parameters.STATUS:
            return Task.get(status=parametr_value)

    if parameter == Parameters.TAGS:
            tasks = select(t for t in Task
                           if user_id in t.users).prefetch(Task.title)

            pickled_data = cPickle.dumps(tasks)
            tasks = cPickle.loads(pickled_data)

            lst = []

            for task in tasks:
                if task.tags != "":
                    list_of_tags = map(lambda tag: tag.strip(), task.tags.split(","))
                    if parametr_value in list_of_tags:
                        lst.append(task)
            return lst


@db_session
def get_tasks(user_id: int):
    tasks = (select(task for task in Task).prefetch(Task))

    tasks_lst = []

    for task in tasks:
        if isinstance(task, Task):
            for u in task.users:
                if u == user_id:
                    tasks_lst.append({'id': task.id, 'type': "Task", 'title': task.title, 'text': task.text,
                                 'status': task.status, 'tags': task.tags, 'date': task.date,
                                 'parent_id': task.parent_id, 'creator': task.creator})

        if isinstance(task, PeriodicTask):
            for u in task.users:
                if u == user_id:
                    tasks_lst.append({'id': task.id, 'type': "PeriodicTask", 'title': task.title, 'text': task.text,
                                'status': task.status, 'tags': task.tags, 'start_date': task.start_date,
                                'period': task.period, 'date': task.date, 'parent_id': task.parent_id,
                                'creator': task.creator})

    return tasks_lst



#
# @db_session
# def get_task_by_id1(task_id, user_id):
#     tasks = (select(task for task in Task).prefetch(Task))
#
#     tasks_lst = []
#
#     for task in tasks:
#         if isinstance(task, Task):
#             for u in task.users:
#                 if u == user_id:
#                     tasks_lst.append(task)
#                 else:
#                     return errs.TaskNotExistError().code
#
#         if isinstance(task, PeriodicTask):
#             for u in task.users:
#                 if u == user_id:
#                     tasks_lst.append(task)
#                 else:
#                     return errs.TaskNotExistError().code
#
#     return tasks_lst

