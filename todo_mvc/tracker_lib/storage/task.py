from pony.orm import *
import datetime
import pickle
import _pickle as cPickle
import logging
from todo_mvc.tracker_lib.models import User
from todo_mvc.tracker_lib.models import Task
from todo_mvc.tracker_lib.models import PeriodicTask
from todo_mvc.tracker_lib.enums import Parameters
from todo_mvc.tracker_lib.enums import Status
import todo_mvc.tracker_lib.helpers.errors as errs

logger = logging.getLogger('logger')


@db_session
def check_permission(user_id: int, task_id: int):
    """
    Check if task with[task_id] belongs to user with [user_id]
    :param user_id:
    :param task_id:
    :return: bool
    """
    try:
        user = User[user_id]
        task = Task[task_id]
        return user in task.users
    except ObjectNotFound as e:
        raise errs.TaskNotExistError()


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
        if User[user_id] in task.users:
            return True
        else:
            raise errs.TaskWithParentIdNotExistError()
    else:
        raise errs.TaskNotExistError()


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
        if User[user_id] in task.users:
            return True
        else:
            raise errs.TaskWithParentIdNotExistError()
    else:
        raise errs.TaskNotExistError()


@db_session
def get_task_by_id(task_id: int, user_id: int):
    """
    Gets task from database with such [task_id] and converts it to dict
    :param task_id:
    :param user_id:
    :return: task dict() or raise
    """
    if check_permission(user_id=user_id, task_id=task_id):
        task = Task.get(id=task_id)
        logger.info('Get task by id = %s was found!' % task.id)
        return task.to_dict()
    else:
        raise errs.AccessError()


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
    task = Task(creator=user_id, title=title, text=text, status=status, tags=tags,
                date=date, parent_id=parent_id, periodic_task_id=periodic_task_id)
    task.users.add(User[user_id])

    # task = [{'title': task.title, 'text': task.text, 'status': task.status, 'tags': task.tags, 'date': task.date,
    #              'parent_id': task.parent_id, 'periodic_task_id': periodic_task_id, 'creator':task.creator}]

    logger.info('Task, with id = %s was created!' % task.id)

    return task


@db_session
def add_periodic_task(user_id: int, title: str, text:str, status: int, tags: str, start_date: datetime, period: str,
                      date=None, parent_id=None):
    periodic_task = PeriodicTask(creator=user_id, title=title, text=text, status=status, tags=tags, start_date=start_date,
                                 period=period, date=date, parent_id=parent_id)
    periodic_task.users.add(User[user_id])

    # periodic_task= [{'title': periodic_task.title, 'text': periodic_task.text, 'status': periodic_task.status,
    #                       'tags': periodic_task.tags, 'start_date': periodic_task.start_date,
    #                       'period': periodic_task.period, 'date': periodic_task.date, 'parent_id': periodic_task.parent_id, 'creator': periodic_task.creator}]

    logger.info('Periodic Task, with id = %s was created!' % periodic_task.id)

    return periodic_task


@db_session
def get_tasks(user_id: int):
    tasks = select(t for t in Task
                  for user in t.users if user.id == user_id).prefetch(Task.title)
    pickled_data = cPickle.dumps(tasks)
    tasks = cPickle.loads(pickled_data)
    lst = []

    for task in tasks:
        lst.append(task)
    logger.info('Gets all user tasks!')

    return lst


@db_session
def delete_task(user_id: int, task_id: int):
    if check_permission(user_id=user_id, task_id=task_id):
        task = Task[task_id]
        if task.creator == user_id:
            delete(p for p in Task if p.parent_id == task_id)
            task.delete()
            logger.info('Task, with id = %s was deleted!' % task.id)
        else:
            raise errs.UserNotHaveAccessToTask()
    else:
        raise errs.AccessError()


@db_session
def edit_task(user_id: int, task_id: int, enum_parameter_value: Parameters, modified_parameter):
    task = select(t for t in Task
                  for user in t.users if user.id == user_id
                  if t.id == task_id).first()
    pickled_data = cPickle.dumps(task)
    task = cPickle.loads(pickled_data)
    # task = list(task)  # как по-другому достучаться до обьекта

    if task:
        if enum_parameter_value == Parameters.TITLE:
            if type(modified_parameter) is not str:
                raise Exception
            else:
                task.title = modified_parameter
                logger.info('Edit task title with id = %s. New title = %s!' % (task.id, task.title))

        if enum_parameter_value == Parameters.TEXT:
            if type(modified_parameter) is not str:
                raise Exception
            else:
                task.text = modified_parameter
                logger.info('Edit task text with id = %s. New title = %s!' % (task.id, task.text))

        if enum_parameter_value == Parameters.STATUS:
            if type(modified_parameter) is not int:
                raise Exception
            else:
                task.status = modified_parameter
                logger.info('Edit task status with id = %s. New title = %s!' % (task.id, task.status))

        if enum_parameter_value == Parameters.TAGS:
            if type(modified_parameter) is not str:
                raise Exception
            else:
                task.tags = modified_parameter
                logger.info('Edit task tags with id = %s. New title = %s!' % (task.id, task.tags))

        if enum_parameter_value == Parameters.PARENT_ID:
            if type(modified_parameter) is not int:
                raise Exception()
            else:
                task.parent_id = modified_parameter
                logger.info('Edit parent id of task with id = %s. New title = %s!' % (task.id, task.parent_id))
    else:
        raise errs.TaskNotExistError()


@db_session
def get_subtask_of_task(user_id: int, task_id: int):
    tasks = select(t for t in Task
                  for user in t.users if user.id == user_id
                  if t.parent_id == task_id).prefetch(Task.title)
    pickled_data = cPickle.dumps(tasks)
    tasks = cPickle.loads(pickled_data)
    lst = []

    for task in tasks:
        lst.append(task)
    if lst:
        logger.info('Get subtasks of task with id = %s!' % task.id)
        return lst
    else:
        raise errs.AccessError()



@db_session
def share_permission(user_id: int, task_id: int, new_user_id: int):
    if check_permission(user_id=user_id, task_id=task_id):
        task = Task[task_id]
        new_user = User[new_user_id]
        new_user.tasks.add(task)
        tasks = select(t for t in Task
                       for user in t.users if user.id == user_id
                       if t.parent_id == task_id).prefetch(Task.title).prefetch(Task)
        for task in tasks:
            task.users.add(new_user)

        periodic_tasks = select(t for t in Task
                       for user in t.users if user.id == user_id
                       if t.parent_id == task_id).prefetch(Task.title).prefetch(Task)
        for periodic_task in periodic_tasks:
            periodic_task.users.add(new_user)

        logger.info('Share permission to task with id = %s. New user = %s!' % (task.id, new_user.id))
    else:
        raise errs.AccessError()


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
def get_tasks_by_type_of_parameter(user_id: int, parameter: Parameters, parametr_value):
    if parameter == Parameters.TITLE:
        if type(parametr_value) is str:
            tasks = select(t for t in Task
                           for user in t.users if user.id == user_id
                           if t.title == parametr_value)
            pickled_data = cPickle.dumps(tasks)
            tasks = cPickle.loads(pickled_data)
            test = tasks.tag
        else:
            raise Exception()

    if parameter == Parameters.TEXT:
        if type(parametr_value) is str:
            return Task.get(text=parametr_value)
        else:
            raise Exception()

    if parameter.value == 3:
        if type(parametr_value) is Status.value:
            return Task.get(status=parametr_value)
        else:
            raise Exception()

    if parameter == Parameters.TAGS:
            if type(parametr_value) is str:
                tasks = select(t for t in Task
                               for user in t.users if user.id == user_id).prefetch(Task.title)

                pickled_data = cPickle.dumps(tasks)
                tasks = cPickle.loads(pickled_data)

                lst = []

                for task in tasks:
                    if task.tags != "":
                        list_of_tags = map(lambda tag: tag.strip(), task.tags.split(","))
                        if parametr_value in list_of_tags:
                            lst.append(task)
                return lst

    if parameter.value == 5:
        if type(parametr_value) is int:
            return Task.get(parent_id=parametr_value)
        else:
            raise Exception()



