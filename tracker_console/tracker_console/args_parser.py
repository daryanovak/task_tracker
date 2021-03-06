import argparse

from tracker_console.helpers import get_token
from tracker_console.parsers.comment_command_parsers import CommentCommandParsers
from tracker_console.parsers.task_command_parsers import TaskCommandParsers
from tracker_console.parsers.user_command_parsers import UserCommandParsers
from tracker_console.auth.user_controller import UserController


class ArgsParser:
    def __init__(self):
        parser = argparse.ArgumentParser(description='User storage utility')
        subparsers = parser.add_subparsers()
        self.user_controller = UserController()

        self.task_command_parsers = TaskCommandParsers(subparsers)
        self.user_command_parsers = UserCommandParsers(subparsers)
        self.comment_command_parsers = CommentCommandParsers(subparsers)

        if self.user_controller.is_authorized(get_token()):
            self.task_command_parsers.init_authorized_commands()
            self.user_command_parsers.init_authorized_commands()
            self.comment_command_parsers.init_authorized_commands()
        else:
            self.task_command_parsers.init_unauthorized_commands()
            self.user_command_parsers.init_unauthorized_commands()
            self.comment_command_parsers.init_unauthorized_commands()

        self.args = parser.parse_args()

    def command_execute(self):
        self.args.func(self.args)
