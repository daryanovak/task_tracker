import logging
import todo_mvc.tracker_lib.helpers.errors as errs
import todo_mvc.tracker_lib.helpers.error_helper as errs_help
from console.helpers import get_token
from todo_mvc.tracker_lib.controllers.comment import CommentController
from todo_mvc.tracker_lib.controllers.user import UserController

logger = logging.getLogger(__name__)


class CommentView:
    def __init__(self):
        self.user_controller = UserController()
        self.controller = CommentController()

    def create_comment_of_task(self, args):
        try:
            self.controller.create_comment_of_task(args.task_id, args.text, args.date)
        except (errs.AccessError, errs.TaskNotExistError) as e:
            errs_help.console_print(e)
            logger.error(e.name)

    def get_comments_of_task(self, args):
        try:
            comments = self.controller.get_comments_of_task(args.task_id)
            for comment in comments:
                print(comment)
        except errs.TaskNotExistError as e:
            errs_help.console_print(e)
            logger.error(e.name)
