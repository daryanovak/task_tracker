from datetime import datetime
from enum import Enum

from pony.orm import *
from tracker_lib.helpers.storage_helper import StorageHelper

from .database import db


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


class Task(db.Entity):
    def __str__(self):
        return self.title and (str(self.id) + ' '+ self.title + ' ' + self.text + ' ' + str(self.status) + ' '
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
    periodic_task_id = Optional(int)
    users = Required(Json)


class PeriodicTask(Task):
    start_date = Required(datetime)
    period = Required(str)


class Comment(db.Entity):
    id = PrimaryKey(int, auto=True)
    text = Required(LongStr)
    user_id = Required(int)
    task = Required(Task)


db.generate_mapping(create_tables=True)