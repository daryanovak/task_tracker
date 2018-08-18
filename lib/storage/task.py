from pony.orm import *
import datetime
import pickle
import _pickle as cPickle
from lib.models import User
from lib.models import Task
from lib.models import PeriodicTask
from lib.enums import Parameters
from lib.enums import Status
import lib.helpers.errors as errs
import re
from lib.helpers.cron_period_helper import CronPeriodHelper


@db_session
def check_permission(user_id, task_id):
    try:
        user = User[user_id]
        task = Task[task_id]
        return user in task.users
    except ObjectNotFound as e:
        raise errs.TaskNotExistError()

@db_session
def get_task_by_id(task_id, user_id):
    if check_permission(user_id=user_id, task_id=task_id):
        task = Task.get(id=task_id)
        return task.to_dict()
    else:
        raise errs.AccessError()


@db_session
def add_task(user_id: int, title: str, text: str, status: int, tags: str, date=None, parent_id=None):
    task = Task(creator=user_id, title=title, text=text, status=status, tags=tags, date=date, parent_id=parent_id)
    task.users.add(User[user_id])


@db_session
def add_periodic_task(user_id: int, title, text, status, tags, start_date, period, date=None, parent_id=None):
     periodic_task = PeriodicTask(creator=user_id, title=title, text=text, status=status, tags=tags, start_date=start_date,
                                 period=period, date=date, parent_id=parent_id)
     periodic_task.users.add(User[user_id])


@db_session
def get_tasks(user_id):
    tasks = select(t for t in Task
                  for user in t.users if user.id == user_id).prefetch(Task.title)
    pickled_data = cPickle.dumps(tasks)
    tasks = cPickle.loads(pickled_data)
    lst = []

    for task in tasks:
        lst.append(task)

    return lst


@db_session
def delete_task(user_id: int, task_id: int):
    if check_permission(user_id=user_id, task_id=task_id):
        task = Task[task_id]
        task.delete()
    else:
        raise errs.AccessError()

    # task = select(t for t in Task
    #               for user in t.users if user.id == user_id
    #               if t.id == task_id)
    #
    # pickled_data = cPickle.dumps(task)
    # task = cPickle.loads(pickled_data)
    # tasks = list(task)  # как по-другому достучаться до обьекта
    # if tasks:
    #     tasks[0].delete()
    # else:
    #     raise Exception()


@db_session
def edit_task(user_id, task_id, enum_parameter_value: Parameters, modified_parameter):
    task = select(t for t in Task
                  for user in t.users if user.id == user_id
                  if t.id == task_id)
    pickled_data = cPickle.dumps(task)
    task = cPickle.loads(pickled_data)
    task = list(task)  # как по-другому достучаться до обьекта

    if task:
        if enum_parameter_value.value == 1:
            if type(modified_parameter) is not str:
                raise Exception
            else:
                task[0].title = modified_parameter

        if enum_parameter_value == Parameters.TEXT:
            if type(modified_parameter) is not str:
                raise Exception
            else:
                task[0].text = modified_parameter

        if enum_parameter_value == Parameters.STATUS:
            if type(modified_parameter) is not int:
                raise Exception
            else:
                task[0].status = modified_parameter

        if enum_parameter_value == Parameters.TAGS:
            if type(modified_parameter) is not str:
                raise Exception
            else:
                task[0].tags = modified_parameter

        if enum_parameter_value == Parameters.PARENT_ID:
            if type(modified_parameter) is not int:
                raise Exception()
            else:
                task[0].parent_id = modified_parameter
    else:
        raise errs.TaskNotExistError()


@db_session
def get_subtask_of_task(user_id, task_id):
    tasks = select(t for t in Task
                  for user in t.users if user.id == user_id
                  if t.parent_id == task_id).prefetch(Task.title)
    pickled_data = cPickle.dumps(tasks)
    tasks = cPickle.loads(pickled_data)
    lst = []

    for task in tasks:
        lst.append(task)

    return lst



@db_session
def share_permission(my_user_id, task_id, new_user_id):
    if check_permission(user_id=my_user_id, task_id=task_id):
        task = Task[task_id]
        new_user = User[new_user_id]
        new_user.tasks.add(task)
    else:
        raise errs.AccessError()

     # tasks = select(t for t in Task
     #               for user in t.users if user.id == my_user_id)
     # pickled_data = cPickle.dumps(tasks)
     # tasks = cPickle.loads(pickled_data)

@db_session
def get_tasks_on_period(user_id, start, end):
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
def get_tasks_by_type_of_parameter(user_id, parameter: Parameters, parametr_value):
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
                        if re.search(parametr_value, task.tags):
                            lst.append(task)
                        else:
                            pass
                    else:
                        pass
                return lst

    if parameter.value == 5:
        if type(parametr_value) is int:
            return Task.get(parent_id=parametr_value)
        else:
            raise Exception()

@db_session
def get_task_id_by_title(title: str):
    return Task.get(title=title)



@db_session
def get_user_id_by_login(login: str):
    return User.get(login=login)




# @db_session
# def delete_task_by_title(user_id, task_id):
#     if check_permission(user_id=user_id, task_id=task_id):
#         Task[task_id].delete()
#     else:
#         raise Exception("NOt ACCESs")


@db_session
def get_task_object_by_title(title):  # получить только свои таски!!!!!!!!!!!!!!!
    task = Task.get(title=title)

    return task


@db_session
def test(title):
    print("LAAAAAAAAAAAAAAAAAAAAAAAa")

