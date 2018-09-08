"""
A module that implements the basic logic of working with the task's comments.
"""
import datetime

import tracker_lib.helpers.errors as errs
import tracker_lib.storage.comment as comment_storage
import tracker_lib.storage.task as task_storage
from tracker_lib.helpers.logging_helper import get_logger

logger = get_logger()


class CommentController:
    """

    Class CommentControllers takes one parameter user_id, which allows works with users logic.

    """
    def __init__(self, user_id):
        self.user_id = user_id

    def create_task_comment(self, task_id: int, text: str, date: datetime =None):
        """

        Creates Comment () for task with task_id which belongs to user with user_id.
        Checks if the user have access to task, and then create comment.
        Comment for a periodic task creates with help --date parameter.

        :param task_id: task_id
        :param text: text of comment
        :param date: date of the periodic task to which you want to apply
        """
        if not task_storage.check_permission(user_id=self.user_id, task_id=task_id):
            logger.error(errs.AccessError().name)
            raise errs.AccessError()

        if date:
            comment_storage.create_periodic_task_comment(user_id=self.user_id, task_id=task_id, text=text,
                                                         date=date)

            logger.info('Was created comment for periodic task with id =  = %s!' % task_id)

        else:
            comment_storage.create_task_comment(user_id=self.user_id, text=text, task_id=task_id)

            logger.info('Was created comment for task with id =  = %s!' % task_id)

    def get_task_comments(self, task_id: int):
        """

        Gets all comment of task by id.
        Method checks, if user have access to task, and then returns all it's comment

        :param task_id: task id
        :return: all task of comment and their creators
        """
        if not task_storage.check_permission(user_id=self.user_id, task_id=task_id):
            logger.error(errs.AccessError().name)
            raise errs.AccessError()

        #logger.info('Gets comment of task id =!' % task_id)

        return comment_storage.get_task_comments(task_id=task_id)

    def check_user_in_comment(self, user_id, comment_id):
        """

        Checks if user have access to comment.
        If it has, return true, else raises exception

        :param user_id: user id
        :param comment_id: comment id
        :return: return True, if user have access or exception
        """
        return_value = comment_storage.check_user_in_comment(user_id=user_id, comment_id=comment_id)
        if return_value == errs.CommentNotFoundError().code:
            raise errs.CommentNotFoundError()
        if return_value == errs.CommentAccessError().code:
            raise errs.CommentAccessError()
        if return_value:
            return True
