import todo_mvc.tracker_lib.storage.comment as comment_storage
import todo_mvc.tracker_lib.storage.task as task_storage
import todo_mvc.tracker_lib.helpers.errors as errs
from  tracker_lib.controllers.task import TaskController
import datetime
import logging

logger = logging.getLogger('logger')


class CommentController:
    def __init__(self, user_id):
        self.user_id = user_id

    def create_comment_of_task(self, task_id: int, text: str, date: datetime):
        """
        Creates comment for task by his id
        :param task_id: task_id
        :param text: text of comment
        :param date: date of the periodic task to which you want to apply
        """
        if task_storage.check_permission(user_id=self.user_id, task_id=task_id):

            if date:
                comment_storage.create_comment_for_periodic_task(user_id=self.user_id, task_id=task_id, text=text,
                                                                 date=date)

                logger.info('Was created comment for periodic task with id =  = %s!' % task_id)

            else:
                comment_storage.create_comment_for_task(user_id=self.user_id, text=text, task_id=task_id)

                logger.info('Was created comment for task with id =  = %s!' % task_id)

        else:
            logger.error(errs.AccessError().name)
            raise errs.AccessError()

    def get_comments_of_task(self, task_id: int):
        """
        Gets all comment of task by id
        :param user_id: user_id
        :param task_id: task id
        :return: tasks
        """
        if task_storage.check_permission(user_id=self.user_id, task_id=task_id):

            # logger.info('Gets comment of task id =!' % task_id)

            return comment_storage.get_comments_of_task(task_id=task_id)

        else:
            logger.error(errs.AccessError().name)
            raise errs.AccessError()

    def check_is_it_user_comment(self, user_id, comment_id):
        return_value = comment_storage.check_is_it_user_comment(user_id=user_id, comment_id=comment_id)
        if return_value:
            return True
        if return_value == errs.CommentAccessError().code:
            raise errs.CommentAccessError()

    def delete_comment(self, comment_id: int):
        if self.check_is_it_user_comment(user_id=self.user_id, comment_id=comment_id):

            return_value = comment_storage.delete_comment(user_id=self.user_id, comment_id=comment_id)

            if return_value == errs.CommentAccessError().code:
                raise errs.CommentAccessError()
            if return_value:
                logger.info('Delete comment with commnet_id %s' % str(comment_id))

        else:
            logger.error(errs.CommentAccessError().name)
            raise errs.CommentAccessError()
