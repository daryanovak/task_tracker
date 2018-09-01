from tracker_console.views.task import TaskView


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
        self.edit_task_parser()
        self.share_task_permission_parser()

    def init_unauthorized_commands(self):
        pass

    def create_task_parser(self):
        parser_append = self.subparsers.add_parser('create_task', help='Creates new task')
        parser_append.add_argument('title', help='title task', default='Title')
        parser_append.add_argument('text', help='text task', default='Empty text')
        parser_append.add_argument('status', help='task status {Planed = 0, Completed = 1, Failed = 2}', default='0', choices=['0', '1', '2'])
        parser_append.add_argument('--tags', help='tags', default='')
        parser_append.add_argument('--parent_id', help='parent id', default='')
        parser_append.add_argument('--date', help="date in format 'd/m/y H:M", default=0)

        parser_append.set_defaults(func=self.view.create_new_task)

    def create_periodic_task_parser(self):
        parser_append = self.subparsers.add_parser('create_periodic_task', help='Creates new tasks.py')
        parser_append.add_argument('title', help='title', default='Title')
        parser_append.add_argument('text', help='text', default='Empty text')
        parser_append.add_argument('status', help='task status {Planed = 0, Completed = 1, Failed = 2}', default='0',
                                   choices=[0, 1, 2])
        parser_append.add_argument('start_date', help="start date date in format 'd/m/y H:M", default="")
        parser_append.add_argument('date', help=" deadline date in format 'd/m/y H:M", default=0)
        parser_append.add_argument('period', help='cron period', default="")
        parser_append.add_argument('--tags', help='tags', default='')
        parser_append.add_argument('--parent_id', help='parent id', default=None)

        parser_append.set_defaults(func=self.view.create_new_periodic_task)

    def delete_task_parser(self):
        parser_append = self.subparsers.add_parser('delete_task', help='Deletes task')
        parser_append.add_argument('task_id', help='task id', default='')
        parser_append.set_defaults(func=self.view.delete_task)

    def get_tasks_parser(self):
        parser_append = self.subparsers.add_parser('get_tasks', help='Shows all tasks of current user')
        parser_append.set_defaults(func=self.view.get_tasks)

    def get_task_by_id_parser(self):
        parser_append = self.subparsers.add_parser('task_by_id', help='Gets task by id')
        parser_append.add_argument('task_id', help='task id', default='')
        parser_append.set_defaults(func=self.view.get_task_by_id)

    def edit_task_parser(self):
        parser_append = self.subparsers.add_parser('edit_task', help='Edits task by parameter')
        parser_append.add_argument('task_id', help='task id', default=None)
        parser_append.add_argument('parameter', help='enum.Parameter TITLE = 1,TEXT = 2, STATUS = 3,TAGS = 4,'
                                                     ' PARENT_ID = 5', default=None)
        parser_append.add_argument('new_parameter', help='new value of parameter', default=' ')
        parser_append.set_defaults(func=self.view.edit_task)

    def get_subtasks_parser(self):# возврщает повторяющиеся при раздаче
        parser_append = self.subparsers.add_parser('get_subtasks', help='Gets subtasks of task')
        parser_append.add_argument('task_id', help='task id', default='task id')
        parser_append.set_defaults(func=self.view.get_task_subtasks)

    def share_task_permission_parser(self):
        parser_append = self.subparsers.add_parser('share_permission', help='Share permission to user')
        parser_append.add_argument('new_user_id', help='new user id', default='Login of users')
        parser_append.add_argument('task_id', help='task id', default='task id')
        parser_append.set_defaults(func=self.view.share_task_permission)

    def get_tasks_by_tag_parser(self):
        parser_append = self.subparsers.add_parser('by_tag', help='Returns tasks with such tag')
        parser_append.add_argument('tag', help='tag value', default='Login of users')
        parser_append.set_defaults(func=self.view.get_tasks_by_tag)

    def get_tasks_on_period_parser(self):
        parser_append = self.subparsers.add_parser('tasks_on_period', help='Returns tasks by period')
        parser_append.add_argument('start', help='start date of period', default='')
        parser_append.add_argument('end', help='end date of period', default='')
        parser_append.set_defaults(func=self.view.get_tasks_on_period)

