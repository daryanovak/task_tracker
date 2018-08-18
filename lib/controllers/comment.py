import lib.storage.comment as comment_storage
import lib.storage.user as user_storage
import datetime


class CommentController():
    def create_comment_of_task(self, task_id, text):
        current_user_id = user_storage.get_current_user()
        date = datetime.datetime.now()
        comment_storage.create_comment_of_task(user_id=current_user_id, task_id=task_id, text=text, date=date)

    def get_comments_of_task(self,task_id):
        current_user_id = user_storage.get_current_user()
        return comment_storage.get_comments_of_task(user_id=current_user_id, task_id=task_id)
