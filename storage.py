import datetime
from enum import Enum
import _pickle as cPickle
from pony.orm import *


class Parameters(Enum):
    TITLE = 1
    TEXT = 2
    STATUS = 3
    TAGS = 4
    DATE = 5
    PARENT_ID = 6


class Status(Enum):
    PLANNED = 0
    COMPLETED = 1
    FAILED = 2


set_sql_debug(True)

db = Database()


class User(db.Entity):
    login = Required(str, unique=True)
    password = Required(int)
    task = Set('Task')
    comment = Set('Comment', cascade_delete=True)


class Task(db.Entity):
    title = Required(LongStr, unique=True)
    text = Required(str)
    status = Required(int)
    creation_date = Required(datetime.datetime)
    tags = Optional(str)
    date = Optional(datetime.timedelta)
    parent_id = Optional(int)
    comment = Set('Comment', cascade_delete=True)
    user = Set('User')


class PeriodicTask(Task):
    start_date = Required(datetime.timedelta)
    period = Required(str)


class Comment(db.Entity):
    text = Required(LongStr)
    user = Required(User)
    task = Required(Task)


db.bind('sqlite', 'test_.sqlite', create_db=True)
# db.bind('postgres', user='postgres', password='postgres', host='localhost', database='mydb')

db.drop_table("Numbers", if_exists=True, with_all_data=True)
db.generate_mapping(create_tables=True)


@db_session
def add_task(title: str, text: str, status: int, tags: str, date=None, parent_id=None):
    """
    Creates a new task
    :param title: task title
    :param text: task text
    :param status: status
        PLANNED = 0
        COMPLETED = 1
        FAILED = 2
    :param tags: task tegs
    :param date: planned date of created task
    :param parent_id: optional parameter, which means than current task is subtask of task with this parent_id
    """
    Task(title=title, text=text, status=status, tags=tags, date=date, parent_id=parent_id,
         creation_date=datetime.datetime.now())


@db_session
def add_periodic_task(title, text, status, tags, start_date, period, date=None, parent_id=None):
    """
    Creates a new periodic task
    :param title:
    :param text:
    :param status:
    :param tags:
    :param start_date: starts
    :param period: period of repeat
    :param date: ends
    :param parent_id:
    """
    PeriodicTask(title=title, text=text, status=status, tags=tags,
                 start_date=start_date, period=period, date=date, parent_id=parent_id,
                 creation_date=datetime.datetime.now())


@db_session
def add_user(login, password):
    """
    Creates a new user
    :param login: unique login
    :param password: password
    """
    User(login=login, password=password)


@db_session
def check_permission(user_id, task_id):
    user = User[user_id]
    task = Task[task_id]
    print("++++++++++++++++++++++++++++++++++++++++")
    print(task.user)
    print(user in task.user)
    return user in task.user


@db_session
def add_comment(text, user_id, task_id):  # проверки можно ли писать данному пользователю комментарий
    """
    Creates a comment for task
    :param text:
    :param user_id:
    :param task_id:
    """
    if check_permission(user_id=user_id, task_id=task_id):
        Comment(text=text, user=User[user_id], task=Task[task_id])
    else:
        raise Exception("NOT notttttttt")


@db_session
def delete_task(user_id, task_id):
    if check_permission(user_id=user_id, task_id=task_id):
        Task[task_id].delete()
    else:
        raise Exception("NOt ACCESs")


@db_session
def delete_user(user_id):  # Проверка только для суперпользователя
    User[user_id].delete()


@db_session
def delete_comment(user_id, comment_id):
    if User[user_id] is Comment[comment_id].user:
        Comment[comment_id].delete()
    else:
        raise Exception("NOT ACCESS TO COMMENT")


@db_session
def get_task_object_by_title(title):  # получить только свои таски!!!!!!!!!!!!!!!
    task = Task.get(title=title)
    return task


@db_session
def add_user_to_task(task_id, user_id):  #######только к своим !!!!!!!!!!
    task = Task[task_id]
    task.user.add(User[user_id])


@db_session
def edit_task(user_id, task_id, enum_parameter_value: Parameters, modified_parameter):
    if check_permission(user_id=user_id, task_id=task_id):
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
    else:
        raise Exception("NOT ACCESS")


@db_session
def get_task_by_type_of_parameter(parameter: Parameters, parameter_value):
    if parameter.value == 1:
        if type(parameter_value) is str:
            return Task.get(title=parameter_value)
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
def get_subtask_of_task(user_id, task_id):
    if check_permission(user_id=user_id, task_id=task_id):
        tasks = Task.select(lambda t: t.parent_id == task_id)
        pickled_data = cPickle.dumps(tasks)
        tasks = cPickle.loads(pickled_data)
        print(tasks)
        return tasks
    else:
        raise Exception("NO SUBTASKSSSSSSSss")


with db_session:
    add_task(title="1", text="text1", status=0, tags="life")
    add_task(title="1.1", text="text1.1", status=2, tags="SUBTASK", parent_id=1)
    add_task(title="2", text="text1", status=0, tags="life")
    add_task(title="3", text="text1", status=0, tags="life")
    add_task(title="4", text="4", status=0, tags="lala", date=datetime.timedelta(-1, 68400), parent_id=1)
    add_periodic_task(title="5", text="4", status=0, tags="lala",
                      start_date=datetime.timedelta(-1, 68400), period="period",
                      date=datetime.timedelta(-1, 68400), parent_id=1)
    add_user(login="dasha1", password="333")
    add_user(login="dasha2", password="333")
    add_user(login="dasha3", password="333")

    task = get_task_object_by_title(title="1")
    task2 = get_task_object_by_title(title="2")
    task3 = get_task_object_by_title(title="3")

    add_user_to_task(1, user_id=1)
    add_user_to_task(2, user_id=2)
    add_user_to_task(3, user_id=3)
    add_user_to_task(5, user_id=1)
    add_user_to_task(5, user_id=2)

    add_comment("1comment", 1, 1)
    add_comment("2comment", 2, 2)
    add_comment("3comment", 3, 3)
    add_comment("5comment", 1, 5)
    add_comment("5comment", 2, 5)

    # delete_task(1)
    edit_task(user_id=1, task_id=5, enum_parameter_value=Parameters.TITLE, modified_parameter="EDITEDDDDDDDDDDDDD")
    edit_task(user_id=2, task_id=5, enum_parameter_value=Parameters.TEXT, modified_parameter="MODIFIEDTEXT")
    edit_task(user_id=2, task_id=5, enum_parameter_value=Parameters.STATUS, modified_parameter=Status.FAILED)
    print(get_task_by_type_of_parameter(Parameters.TITLE, "2"))
    # delete_user(2)
    delete_comment(user_id=1, comment_id=1)
    get_subtask_of_task(task_id=1, user_id=1)
