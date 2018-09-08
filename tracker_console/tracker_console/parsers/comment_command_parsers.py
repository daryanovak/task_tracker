from tracker_console.views.comment import CommentView


class CommentCommandParsers:

    def __init__(self, subparsers):
        self.view = CommentView()
        self.subparsers = subparsers

    def init_authorized_commands(self):
        self.create_task_comment()
        self.get_task_comments()

    def init_unauthorized_commands(self):
        pass

    def create_task_comment(self):
        parser_append = self.subparsers.add_parser('comment_task', help='Creates comment for task')
        parser_append.add_argument('task_id', help='task id', default='')
        parser_append.add_argument('text', help='comment text', default='')
        parser_append.add_argument('--date', help='date of periodic task, which you comment', default='')
        parser_append.set_defaults(func=self.view.create_task_comment)

    def get_task_comments(self):
        parser_append = self.subparsers.add_parser('get_comments', help='Returns all comments for task')
        parser_append.add_argument('task_id', help='', default='task id')
        parser_append.set_defaults(func=self.view.get_task_comments)