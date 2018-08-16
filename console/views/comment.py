# import typing
# import lib.helpers.error_helper as err_help
# import lib.models.errors as errs
"""
from todo_mvc.tracker_lib.lib.controllers.comment_controller import CommentController
from todo_mvc.tracker_lib.lib.controllers.user_controller import UserCont
from todo_mvc.config import configroller
from todo_mvc.tracker_lib.lib.models.сomment import Comment
from todo_mvc.tracker_lib.lib.models.task import Task
"""

import logging
logger = logging.getLogger(__name__)


class CommentView:
    def __init__(self):
        pass
        #self.controller = CommentController(config['db_path'], UserController(config['db_path']).get_current_user())

    def create_comment_of_task(self, args):
      """
         task: Task = self.controller.find_task_by_title(args.title)
        self.controller.create_comment_of_task(task.id, args.text, args.date)

      """
    def get_comments_of_task(self, args):
      """
       try:
            task: Task = self.controller.find_task_by_title(args.title)
            comments: typing.List[Comment] = self.controller.get_comments_of_task(task.id)
            for comment in comments:
                print(comment.owner + ': ' + comment.text)
        except errs.TitleError as e:
            err_help.console_print(e)
            logger.error(e.name)
      """
