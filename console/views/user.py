from console.helpers import get_token
from todo_mvc.tracker_lib.controllers.user import UserController
import logging
import todo_mvc.tracker_lib.helpers.errors as errs
import todo_mvc.tracker_lib.helpers.error_helper as errs_help

logger = logging.getLogger('logger')


class UserView:
    def __init__(self):
        self.controller = UserController()

    def log_in(self, args):
        try:
            token = self.controller.log_in(args.login, args.password)
            with open("./console/token", "w+") as file:
                file.writelines(token)
        except errs.UserLoginError as e:
            errs_help.console_print(e)
            logger.error(e.name)

    def create_user(self, args):
        self.controller.sign_up(args.login, args.password)

    def log_out(self):
        self.controller.log_out(self.controller.user_id(get_token()))
        with open('./console/token', 'r+') as file:
            file.truncate()

    def delete_user(self, args):
        pass
