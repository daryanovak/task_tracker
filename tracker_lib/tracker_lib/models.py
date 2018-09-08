from datetime import datetime

from pony.orm import (
    Required,
    Optional,
    Set,
    Json,
    PrimaryKey,
    LongStr
)

from .database import db


def datetime_to_str(date):
    if date:
        return date.strftime("%d/%m/%y %H:%M")
    else:
        return " "


class Task(db.Entity):
    def __str__(self):
        return self.title and (str(self.id) + ' ' + self.title + ' ' + self.text + ' ' + str(self.status) + ' '
                               + self.tags + ' ' + datetime_to_str(self.date))
    id = PrimaryKey(int, auto=True)
    creator = Required(int)
    title = Required(str)
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