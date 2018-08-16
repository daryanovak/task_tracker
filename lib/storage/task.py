from pony.orm import db_session
import datetime
import _pickle as cPickle
from lib.models import User
from lib.models import Task
from lib.models import PeriodicTask
from lib.enums import Parameters
from lib.enums import Status


@db_session
def check_permission(user_id, task_id):
    user = User[user_id]
    task = Task[task_id]
    print("++++++++++++++++++++++++++++++++++++++++")
    print(task.user)
    print(user in task.user)
    return user in task.user


@db_session
def add_task(user_id: int, title: str, text: str, status: int, tags: str, date=None, parent_id=None):
    task = Task(creator=user_id, title=title, text=text, status=status, tags=tags, date=date, parent_id=parent_id)



@db_session
def add_periodic_task(user_id: int, title, text, status, tags, start_date, period, date=None, parent_id=None):
    periodic_task = PeriodicTask(creator=user_id, title=title, text=text, status=status, tags=tags, start_date=start_date,
                                 period=period, date=date, parent_id=parent_id)


@db_session
def get_task_id_by_title(title: str):
    return Task.get(title=title)


@db_session
def get_user_id_by_login(login: str):
    return User.get(login=login)


@db_session
def get_subtask_of_task(user_id, task_id):
    # if check_permission(user_id=user_id, task_id=task_id):
        tasks = Task.select(lambda t: t.parent_id == task_id)
        pickled_data = cPickle.dumps(tasks)
        tasks = cPickle.loads(pickled_data)
        print(tasks)
        return tasks
    # else:
    #     raise Exception("NO SUBTASKSSSSSSSss")


@db_session
def edit_task(user_id, task_id, enum_parameter_value: Parameters, modified_parameter):
    # if check_permission(user_id=user_id, task_id=task_id):
        task = Task[task_id]

        if enum_parameter_value.value == 1:
            if type(modified_parameter) is not str:
                raise Exception
            else:
                task.title = modified_parameter

        if enum_parameter_value.value == 2:
            if type(modified_parameter) is not str:
                raise Exception
            else:
                task.text = modified_parameter

        if enum_parameter_value.value == 3:
            if type(modified_parameter) is not Status:
                raise Exception
            else:
                task.status = modified_parameter.value

        if enum_parameter_value.value == 4:
            if type(modified_parameter) is not str:
                raise Exception
            else:
                task.tags = modified_parameter

        if enum_parameter_value == 5:
            if type(modified_parameter) is not datetime.timedelta:
                raise Exception()
            else:
                task.date = modified_parameter

        if enum_parameter_value == 6:
            if type(modified_parameter) is not int:
                raise Exception()
            else:
                task.parent_id = modified_parameter
    # else:
    #     raise Exception("NOT ACCESS")


@db_session
def delete_task_by_title(user_id, task_id):
    if check_permission(user_id=user_id, task_id=task_id):
        Task[task_id].delete()
    else:
        raise Exception("NOt ACCESs")


@db_session
def get_task_by_type_of_parameter(parameter: Parameters, parameter_value):
    if parameter.value == 1:
        if type(parameter_value) is str:
            task = Task.get(title=parameter_value)
            return task
        else:
            raise Exception()

    if parameter_value == 2:
        if type(parameter_value) is str:
            return Task.get(text=parameter_value)
        else:
            raise Exception()

    if parameter_value == 3:
        if type(parameter_value) is Status.value:
            return Task.get(status=parameter_value)
        else:
            raise Exception()

    if parameter_value == 4:
        if type(parameter_value) == 4:
            if type(parameter_value) is str:
                return Task.get(tags=parameter_value)
            else:
                raise Exception()

    if parameter_value == 5:
        if type(parameter_value) is datetime.timedelta:
            return Task.get(date=parameter_value)
        else:
            raise Exception()

    if parameter_value == 6:
        if type(parameter_value) is int:
            return Task.get(parent_id=parameter_value)
        else:
            raise Exception()


@db_session
def get_task_object_by_title(title):  # получить только свои таски!!!!!!!!!!!!!!!
    task = Task.get(title=title)
    return task


@db_session
def test(title):
    print("LAAAAAAAAAAAAAAAAAAAAAAAa")


@db_session
def share_permission(my_user_id, task_id, new_user_id):
    task = Task[task_id]
    new_user = User[new_user_id]
    my_user = User[my_user_id]
    #проверить есть ли доступ к таске
    task.user.add(new_user)