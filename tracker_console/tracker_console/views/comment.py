import tracker_lib.helpers.error_helper as errs_help
import tracker_lib.helpers.errors as errs
from tracker_lib.controllers.comment import CommentController

from tracker_console.auth.user_controller import UserController
from tracker_console.helpers import get_token


class CommentView:
    def __init__(self):
        self.user_controller = UserController()
        self.controller = CommentController(self.user_controller.user_id(get_token()))

    def create_task_comment(self, args):
        try:
            self.controller.create_task_comment(args.task_id, args.text, args.date)
        except (errs.AccessError, errs.TaskNotExistError) as e:
            errs_help.console_print(e)

    def get_task_comments(self, args):
        try:
            comments = self.controller.get_task_comments(args.task_id)
            for comment in comments:
                print(comment)
        except errs.TaskNotExistError as e:
            errs_help.console_print(e)
            logger.error(e.name)

    def delete_comment(self, args):
        try:
            self.controller.delete_comment(args.user_id)
        except errs.TaskNotExistError as e:
            errs_help.console_print(e)

