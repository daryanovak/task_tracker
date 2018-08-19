from datetime import datetime

from pony.orm import db_session
import lib.storage.task as task_storage
from lib.models import Task, PeriodicTask, User, Comment
import lib.helpers.errors as errs
from lib.helpers.cron_period_helper import CronPeriodHelper

cph = CronPeriodHelper()

@db_session
def create_comment_of_task(user_id, task_id, text, date):  # проверки можно ли писать данному пользователю комментарий
    task = None
    if task_storage.check_permission(user_id=user_id, task_id=task_id):
        if date:
            task = PeriodicTask[task_id]
            if date and cph.in_period(task.period, date):
                task = task_storage.add_task(user_id, task.title, task.text, task.status, task.tags, datetime.strptime(date, '%d/%m/%y'), task.parent_id, periodic_task_id=task_id)
        else:
            task = Task[task_id]
        user = User[user_id]
        comment = Comment(text=text, user=user, task=task)
        task.comment.add(comment)
    else:
        raise errs.AccessError()

@db_session
def get_comments_of_task(user_id, task_id):
    if task_storage.check_permission(user_id=user_id, task_id=task_id):
        task = Task[task_id]
        comments = task.comment
        comments = list(comments)
        lst = []
        for comment in comments:
            lst.append({'login': comment.user.login, 'text': comment.text})
        return lst
    else:
        raise errs.AccessError()



@db_session
def delete_comment(user_id, comment_id):
    if User[user_id] is Comment[comment_id].user:
        Comment[comment_id].delete()
    else:
        raise Exception("NOT ACCESS TO COMMENT")