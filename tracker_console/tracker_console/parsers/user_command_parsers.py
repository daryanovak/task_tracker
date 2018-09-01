from tracker_console.views.user import UserView


class UserCommandParsers:

    def __init__(self, subparsers):
        self.view = UserView()
        self.subparsers = subparsers

    def init_authorized_commands(self):
        self.log_out_parser()
        self.delete_user_parser()

    def init_unauthorized_commands(self):
        self.log_in_parser()
        self.sign_up_parser()

    def log_in_parser(self):
        parser_append = self.subparsers.add_parser('log_in', help='Log in users')
        parser_append.add_argument('login', help='User login', default='')
        parser_append.add_argument('password', help='User password', default='')
        parser_append.set_defaults(func=self.view.log_in)

    def sign_up_parser(self):
        parser_append = self.subparsers.add_parser('sign_up', help='Sign up')
        parser_append.add_argument('login', help='User login', default='')
        parser_append.add_argument('password', help='User password', default='')
        parser_append.set_defaults(func=self.view.create_user)

    def log_out_parser(self):
        parser_append = self.subparsers.add_parser('log_out', help='Log out')
        parser_append.set_defaults(func=self.view.log_out)

    def delete_user_parser(self):
        parser_append = self.subparsers.add_parser('delete_user', help='Deletes users')
        parser_append.add_argument('user_login', help='User login', default='')
        parser_append.set_defaults(func=self.view.delete_user)

