from tracker_console.helpers import get_token
from tracker_console.auth.user_controller import UserController
import logging
import tracker_lib.helpers.errors as errs
import tracker_lib.helpers.error_helper as errs_help

logger = logging.getLogger('logger')


class UserView:
    def __init__(self):
        self.controller = UserController()

    def log_in(self, args):
        try:
            token = self.controller.log_in(args.login, args.password)
            with open("./tracker_console/token", "w+") as file:
                file.writelines(token)
        except errs.UserLoginError as e:
            errs_help.console_print(e)
            logger.error(e.name)

    def create_user(self, args):
        self.controller.sign_up(args.login, args.password)

    def log_out(self, args):
        self.controller.log_out(self.controller.user_id(get_token()))
        with open('./tracker_console/token', 'r+') as file:
            file.truncate()

    def delete_user(self, args):
        pass
