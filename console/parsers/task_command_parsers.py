from console.views.task import TaskView


class TaskCommandParsers:
    def __init__(self, subparsers):
        self.view = TaskView()
        self.subparsers = subparsers

    def init_authorized_commands(self):
        self.create_task_parser()
        self.create_periodic_task_parser()
        self.get_tasks_parser()
        self.get_task_by_id_parser()
        self.delete_task_parser()
        self.get_tasks_by_tag_parser()
        self.get_subtasks_parser()
        self.get_tasks_on_period_parser()
        self.edit_task_title_parser()
        self.edit_task_text_parser()
        self.edit_task_status_parser()
        self.share_task_permission_parser()

    def init_unauthorized_commands(self):
        pass

    def get_tasks_parser(self):
        parser_append = self.subparsers.add_parser('tasks', help='Get your all notes')
        parser_append.set_defaults(func=self.view.get_tasks)

    def create_task_parser(self):
        parser_append = self.subparsers.add_parser('create_task', help='Create new tasks.py')
        parser_append.add_argument('title', help='Title of tasks.py', default='Title')
        parser_append.add_argument('text', help='Text of tasks.py', default='Empty text')
        parser_append.add_argument('status', help='Complete status', default='0', choices=['0', '1', '2'])
        parser_append.add_argument('--tags', help='Tags', default='')
        parser_append.add_argument('--parent_id', help='Parent title', default='')
        parser_append.add_argument('--date', help="%d/%m/%y %H:%M", default=0)

        parser_append.set_defaults(func=self.view.create_new_task)

    def create_periodic_task_parser(self):
        parser_append = self.subparsers.add_parser('create_periodic_task', help='Create new tasks.py')
        parser_append.add_argument('title', help='Title of tasks.py', default='Title')
        parser_append.add_argument('text', help='Text of tasks.py', default='Empty text')
        parser_append.add_argument('status', help='Complete status', default='0', choices=['0', '1', '2'])
        parser_append.add_argument('start_date', help="%d/%m/%y %H:%M", default="")
        parser_append.add_argument('date', help="%d/%m/%y %H:%M", default=0)
        parser_append.add_argument('period', help='Cron period', default="")
        parser_append.add_argument('--tags', help='Tags', default='')
        parser_append.add_argument('--parent_id', help='Parent title', default=None)

        parser_append.set_defaults(func=self.view.create_new_periodic_task)

    def delete_task_parser(self):
        parser_append = self.subparsers.add_parser('delete_task', help='Delete task')
        parser_append.add_argument('task_id', help='id', default='')
        parser_append.set_defaults(func=self.view.delete_task)

    def get_tasks_parser(self):
        parser_append = self.subparsers.add_parser('get_tasks', help='Show tasks')
        parser_append.set_defaults(func=self.view.get_tasks)

    def get_task_by_id_parser(self):
        parser_append = self.subparsers.add_parser('task_by_id', help='Get tasks.py by title')
        parser_append.add_argument('task_id', help='task id', default='')
        parser_append.set_defaults(func=self.view.get_task_by_id)

    def edit_task_title_parser(self):
        parser_append = self.subparsers.add_parser('edit_task_title', help='Edit title')
        parser_append.add_argument('task_id', help='task id', default=None)
        parser_append.add_argument('new_title', help='new title', default='Title')
        parser_append.set_defaults(func=self.view.edit_task_title)

    def edit_task_text_parser(self):
        parser_append = self.subparsers.add_parser('edit_task_text', help='Edit text')
        parser_append.add_argument('task_id', help='task id', default='Title')
        parser_append.add_argument('new_text', help='New text', default='Text')
        parser_append.set_defaults(func=self.view.edit_task_text)

    def edit_task_status_parser(self):
        parser_append = self.subparsers.add_parser('edit_task_status', help='Edit status')
        parser_append.add_argument('task_id', help='task id', default='Title')
        parser_append.add_argument('new_status', help='New status', default='Text')
        parser_append.set_defaults(func=self.view.edit_task_status)

    def get_subtasks_parser(self):
        parser_append = self.subparsers.add_parser('subtasks_of_task', help='Gets subtasks')
        parser_append.add_argument('task_id', help='task id', default='task id')
        parser_append.set_defaults(func=self.view.get_subtasks_of_task)

    def share_task_permission_parser(self):
        parser_append = self.subparsers.add_parser('share_permission', help='Share permission')
        parser_append.add_argument('new_user_id', help='', default='Login of users')
        parser_append.add_argument('task_id', help='task id', default='task id')
        parser_append.set_defaults(func=self.view.share_task_permission)

    def get_tasks_by_tag_parser(self):#log info
        parser_append = self.subparsers.add_parser('by_tag', help='Search by tag')
        parser_append.add_argument('tag', help='', default='Login of users')
        parser_append.set_defaults(func=self.view.get_tasks_by_tag)

    def get_tasks_on_period_parser(self):#log_info
        parser_append = self.subparsers.add_parser('tasks_on_period', help='tasks on period')
        parser_append.add_argument('start', help='', default='')
        parser_append.add_argument('end', help='', default='')
        parser_append.set_defaults(func=self.view.get_tasks_on_period)

