# import typing
# import lib.helpers.error_helper as err_help
# import lib.models.errors as errs
"""
from todo_mvc.tracker_lib.lib.controllers.comment_controller import CommentController
from todo_mvc.tracker_lib.lib.controllers.user_controller import UserCont
from todo_mvc.config import configroller
from todo_mvc.tracker_lib.lib.models.сomment import Comment
from todo_mvc.tracker_lib.lib.models.tasks import Task
"""

import logging
logger = logging.getLogger(__name__)
from lib.controllers.comment import CommentController
import lib.helpers.errors as errs
import lib.helpers.error_helper as errs_help


class CommentView:
    def __init__(self):
        self.controller = CommentController()

    def create_comment_of_task(self, args):
        try:
            self.controller.create_comment_of_task(args.task_id, args.text, args.date)
        except errs.AccessError as e:
            errs_help.console_print(e)

    def get_comments_of_task(self, args):
        try:
            comments = self.controller.get_comments_of_task(args.task_id)
            for comment in comments:
                print(comment)
        except errs.AccessError as e:
            errs_help.console_print(e)
