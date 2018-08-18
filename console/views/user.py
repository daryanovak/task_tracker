from lib.controllers.user import UserController
import logging
import os
import lib.helpers.errors as errs
import lib.helpers.error_helper as errs_help

logger = logging.getLogger('logger')


class UserView:
    def __init__(self):
        self.controller = UserController()

    def log_in(self, args):
        try:
            self.controller.log_in(args.login, args.password)
        except errs.UserLoginError as e:
            errs_help.console_print(e)

    def create_user(self, args):
        self.controller.sign_up(args.login, args.password)
        # args = ParseHelper.parse_args(args)
        # users = User(**args)
        # self.controller.create_user(users)

    def log_out(self, args):
        self.controller.log_out()
        # self.controller.log_out()

    # Super users

    def delete_user(self, args):
        pass
        # try:
        #     self.controller.delete_user(args.user_login)
        # except errs.AccessError as e:
        #     err_help.console_print(e)