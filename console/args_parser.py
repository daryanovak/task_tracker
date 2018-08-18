import argparse
import os
from console.parsers.comment_command_parsers import CommentCommandParsers
from console.parsers.task_command_parsers import TaskCommandParsers
from console.parsers.user_command_parsers import UserCommandParsers
# from todo_mvc.tracker_lib.lib.controllers.user_controller import UserController
# from todo_mvc.config import config


class ArgsParser:
    def __init__(self):
        """Настройка argparse"""
        parser = argparse.ArgumentParser(description='User storage utility')
        subparsers = parser.add_subparsers()

        #self.user_controller = UserController(config['db_path'])
        self.task_command_parsers = TaskCommandParsers(subparsers)
        self.user_command_parsers = UserCommandParsers(subparsers)
        self.comment_command_parsers = CommentCommandParsers(subparsers)

        if os.stat("lib/token").st_size != 0:
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
