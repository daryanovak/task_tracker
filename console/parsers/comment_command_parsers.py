from console.views.comment import CommentView


class CommentCommandParsers:

    def __init__(self, subparsers):
        self.view = CommentView()
        self.subparsers = subparsers

    def init_authorized_commands(self):
        self.create_comment_of_task()
        self.get_comments_of_task()

    def init_unauthorized_commands(self):
        pass

    def create_comment_of_task(self):
        parser_append = self.subparsers.add_parser('comment_task', help='comment note')
        parser_append.add_argument('task_id', help='', default='Title of note')
        parser_append.add_argument('text', help='', default='Text of comment')
        parser_append.add_argument('--date', help='', default='')
        parser_append.set_defaults(func=self.view.create_comment_of_task)

    def get_comments_of_task(self):#непонятный обьект создается
        parser_append = self.subparsers.add_parser('comments_of_task', help='comment note')
        parser_append.add_argument('task_id', help='', default='Title of note')
        parser_append.set_defaults(func=self.view.get_comments_of_task)


