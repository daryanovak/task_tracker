from pony.orm import *
from lib.database import db
from enum import Enum
from datetime import datetime
from lib.helpers.storage_helper import StorageHelper


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


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    login = Required(str, unique=True)
    password = Required(int)
    token = Optional(LongStr)
    tasks = Set('Task')
    comment = Set('Comment', cascade_delete=True)


class Task(db.Entity):
    def __str__(self):
        return self.title and (self.id + ' '+ self.title + ' ' + self.text + ' ' + str(self.status) + ' '
                               + self.tags + ' ' + StorageHelper.datetime_to_str(self.date))
    id = PrimaryKey(int, auto=True)
    creator = Required(int)
    title = Required(LongStr)
    text = Required(str)
    status = Required(int)
    tags = Optional(str)
    date = Optional(datetime)
    parent_id = Optional(int)
    comment = Set('Comment', cascade_delete=True)
    users = Set('User')


class PeriodicTask(Task):
    start_date = Required(datetime)
    period = Required(str)


class Comment(db.Entity):
    id = PrimaryKey(int, auto=True)
    text = Required(LongStr)
    user = Required(User)
    date = Required(datetime)
    task = Required(Task)


db.generate_mapping(create_tables=True)