import logging
import todo_mvc.tracker_lib.helpers.errors as errs
import todo_mvc.tracker_lib.helpers.error_helper as errs_help
from console.helpers import get_token
from todo_mvc.tracker_lib.controllers.comment import CommentController
from console.auth.user_controller import UserController

logger = logging.getLogger(__name__)


class CommentView:
    def __init__(self):
        self.user_controller = UserController()
        self.controller = CommentController(self.user_controller.user_id(get_token()))

    def create_comment_of_task(self, args):
        try:
            self.controller.create_comment_of_task(args.task_id, args.text, args.date)
        except (errs.AccessError, errs.TaskNotExistError) as e:
            errs_help.console_print(e)

    def get_comments_of_task(self, args):
        try:
            comments = self.controller.get_comments_of_task(args.task_id)
            for comment in comments:
                print(comment)
        except errs.TaskNotExistError as e:
            errs_help.console_print(e)
            logger.error(e.name)

    def delete_comment(self, args):
        try:
            self.controller.delete_comment(args.comment_id)
        except (errs.CommentNotFoundError, errs.CommentAccessError) as e:
            errs_help.console_print(e)

