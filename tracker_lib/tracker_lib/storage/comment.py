from datetime import datetime

from pony.orm import (
    ObjectNotFound,
    db_session
)

import tracker_lib.helpers.errors as errs
import tracker_lib.storage.task as task_storage
from tracker_lib.helpers.cron_period_helper import CronPeriodHelper
from tracker_lib.models import (
    Task,
    PeriodicTask,
    Comment
)

cph = CronPeriodHelper()


@db_session
def create_periodic_task_comment(user_id, task_id, text, date):
    if task_storage.check_periodic_task_exist(task_id=task_id, user_id=user_id):
        task = PeriodicTask[task_id]

        if date and cph.in_period(task.period, date):
            task_storage.add_task(user_id=user_id, title=task.title, text=task.text, status=task.status, tags=task.tags,
                                  date=datetime.strptime(date, '%d/%m/%y'), parent_id=task.parent_id,
                                  periodic_task_id=task_id)
        else:
            raise errs.TaskNotExistError()


@db_session
def create_task_comment(user_id, task_id, text):
    task = Task[task_id]
    comment = Comment(text=text, user_id=user_id, task=task)
    task.comment.add(comment)


@db_session
def get_task_comments(task_id):
    task = Task[task_id]
    comments = task.comment
    comments = list(comments)

    lst = [{'login': comment.user_id, 'text': comment.text} for comment in comments]

    return lst


@db_session
def check_user_in_comment(user_id, comment_id):
    try:
        if user_id is Comment[comment_id].user_id:
            return True
        else:
            return errs.CommentAccessError().code
    except ObjectNotFound:
        return errs.CommentNotFoundError().code


@db_session
def delete_comment(user_id, comment_id):
    try:
        Comment[comment_id].delete()
        return True
    except ObjectNotFound:
        return errs.CommentAccessError().code

