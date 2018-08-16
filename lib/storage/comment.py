from pony.orm import db_session
from lib.models import User
from lib.models import Comment

@db_session
def add_comment(text, user_id, task_id):  # проверки можно ли писать данному пользователю комментарий
    """
    Creates a comment for task
    :param text:
    :param user_id:
    :param task_id:
    """
    # if check_permission(user_id=user_id, task_id=task_id):
    Comment(text=text, user=User[user_id], task=Task[task_id])
    # else:
    #     raise Exception("NOT notttttttt")

@db_session
def delete_comment(user_id, comment_id):
    if User[user_id] is Comment[comment_id].user:
        Comment[comment_id].delete()
    else:
        raise Exception("NOT ACCESS TO COMMENT")