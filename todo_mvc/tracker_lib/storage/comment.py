from datetime import datetime
from pony.orm import db_session
import todo_mvc.tracker_lib.storage.task as task_storage
from todo_mvc.tracker_lib.models import Task, PeriodicTask, User, Comment
import todo_mvc.tracker_lib.helpers.errors as errs
from todo_mvc.tracker_lib.helpers.cron_period_helper import CronPeriodHelper
import logging

logger = logging.getLogger('logger')


cph = CronPeriodHelper()


@db_session
def create_comment_for_periodic_task(user_id, task_id, text, date):
    if task_storage.check_periodic_task_exist(task_id=task_id, user_id=user_id):
        task = PeriodicTask[task_id]
        if date and cph.in_period(task.period, date):
            task_storage.add_task(user_id=user_id, title=task.title, text=task.text, status=task.status, tags=task.tags,
                                  date=datetime.strptime(date, '%d/%m/%y'), parent_id=task.parent_id,
                                  periodic_task_id=task_id)
        else:
            raise errs.TaskNotExistError()


@db_session
def create_comment_for_task(user_id, task_id, text):  # проверки можно ли писать данному пользователю комментарий
    task = Task[task_id]
    user = User[user_id]
    comment = Comment(text=text, user=user, task=task)
    task.comment.add(comment)


@db_session
def get_comments_of_task(task_id):
        task = Task[task_id]
        comments = task.comment
        comments = list(comments)
        lst = []
        for comment in comments:
            lst.append({'login': comment.user_id.login, 'text': comment.text})
        return lst


@db_session
def check_is_it_user_comment(user_id, comment_id):
    if User[user_id] is Comment[comment_id].user_id:
        return True
    else:
        raise errs.AccessError()


@db_session
def delete_comment(user_id, comment_id):
    Comment[comment_id].delete()



# @db_session
# def create_comment_of_task(user_id, task_id, text, date):  # проверки можно ли писать данному пользователю комментарий
#     # task = None
#     if date:
#         # if task_storage.check_periodic_task_exist(task_id=task_id, user_id=user_id):
#         #     task = PeriodicTask[task_id]
#         #     if date and cph.in_period(task.period, date):
#         #         task = task_storage.add_task(user_id, task.title, task.text, task.status, task.tags,
#         #                                      datetime.strptime(date, '%d/%m/%y'), task.parent_id,
#         #                                      periodic_task_id=task_id)
#         # else:
#         #     raise errs.TaskNotExistError()
#     else:
#         task = Task[task_id]
#     user = User[user_id]
#     comment = Comment(text=text, user=user, task=task)
#     task.comment.add(comment)
#     logger.info('Was created comment for task with id =  = %s!' % task_id)