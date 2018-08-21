import todo_mvc.tracker_lib.storage.comment as comment_storage
import todo_mvc.tracker_lib.storage.user as user_storage
import datetime


class CommentController:
    # def __init__(self, user_id):
    #     self.user_id = user_id
    def create_comment_of_task(self, user_id: int, task_id: int, text: str, date: datetime):
        """
        Creates comment for task by his id
        :param user_id:
        :param task_id: task_id
        :param text: text of comment
        :param date: date of the periodic task to which you want to apply
        """
        comment_storage.create_comment_of_task(user_id=user_id, task_id=task_id, text=text, date=date)

    def get_comments_of_task(self, user_id: int, task_id: int):
        """
        Gets all comment of task by id
        :param user_id: user_id
        :param task_id: task id
        :return: tasks
        """
        return comment_storage.get_comments_of_task(user_id=user_id, task_id=task_id)
