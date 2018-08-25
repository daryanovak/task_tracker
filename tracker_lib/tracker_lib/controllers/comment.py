"""
A module that implements the basic logic of working with the task's comments.
"""
import datetime
import logging

import tracker_lib.helpers.errors as errs
import tracker_lib.storage.comment as comment_storage
import tracker_lib.storage.task as task_storage

logger = logging.getLogger('logger')


class CommentController:
    """
    Class CommentControllers takes one parameter user_id, which allows works with users logic.

    """
    def __init__(self, user_id):
        self.user_id = user_id

    def create_task_comment(self, task_id: int, text: str, date: datetime):
        """

        Creates Comment () for task with task_id which belongs to user with user_id.
        Checks if the user have access to task, and then create comment.
        Comment for a periodic task creates with help --date parameter.

        :param task_id: task_id
        :param text: text of comment
        :param date: date of the periodic task to which you want to apply
        """
        if task_storage.check_permission(user_id=self.user_id, task_id=task_id):

            if date:
                comment_storage.create_periodic_task_comment(user_id=self.user_id, task_id=task_id, text=text,
                                                             date=date)

                logger.info('Was created comment for periodic task with id =  = %s!' % task_id)

            else:
                comment_storage.create_task_comment(user_id=self.user_id, text=text, task_id=task_id)

                logger.info('Was created comment for task with id =  = %s!' % task_id)

        else:
            logger.error(errs.AccessError().name)
            raise errs.AccessError()

    def get_task_comments(self, task_id: int):
        """

        Gets all comment of task by id.
        Method checks, if user have access to task, and then returns all it's comment

        :param task_id: task id
        :return: all task of comment and their creators
        """
        if task_storage.check_permission(user_id=self.user_id, task_id=task_id):

            #logger.info('Gets comment of task id =!' % task_id)

            return comment_storage.get_task_comments(task_id=task_id)

        else:
            logger.error(errs.AccessError().name)
            raise errs.AccessError()

    def check_user_in_comment(self, user_id, comment_id):
        """

        Checks if user have access to comment.
        If it has, return true, else raises exception

        :param user_id: user id
        :param comment_id: comment id
        :return: return True, if user have access or exception
        """
        return_value = comment_storage.check_user_in_comment(user_id=user_id, comment_id=comment_id)
        if return_value:
            return True
        if return_value == errs.CommentAccessError().code:
            raise errs.CommentAccessError()

    def delete_comment(self, comment_id: int):
        """

        Deletes comment with id = comment_id.
        Checks permission to comment and then if user have access deletes, otherwise raise exception.

        :param comment_id: unique comment id
        """
        if self.check_user_in_comment(user_id=self.user_id, comment_id=comment_id):

            return_value = comment_storage.delete_comment(user_id=self.user_id, comment_id=comment_id)

            if return_value == errs.CommentAccessError().code:
                raise errs.CommentAccessError()
            if return_value:
                logger.info('Delete comment with commnet_id %s' % str(comment_id))

        else:
            logger.error(errs.CommentAccessError().name)
            raise errs.CommentAccessError()
