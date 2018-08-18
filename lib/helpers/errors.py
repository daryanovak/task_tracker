class UserLoginError(Exception):
    def __init__(self):
        self.code = 0
        self.name = "UserLoginError"
        self.desc = "Please check that you have entered your login and password correctly"


class AccessError(Exception):
    def __init__(self):
        self.code = 1
        self.name = "AccessError"
        self.desc = "You don't have access to this task"


class SuperuserError(Exception):
    def __init__(self):
        self.code = 2
        self.name = "SuperuserError"
        self.desc = "Only superuser has access"


class TaskNotExistError(Exception):
    def __init__(self):
        self.code = 3
        self.name = "TaskNotExistError"
        self.desc = "Such task doesn't exist"


class MissedArgumentError(Exception):
    def __init__(self):
        self.code = 4
        self.name = "MissedArgumentError"
        self.desc = "You didn't enter all the arguments of this method"


class AlreadyAuthorizedError(Exception):
    def __init__(self):
        self.code = 5
        self.name = "AlreadyAuthorizedError"
        self.desc = "You are already logged in"


class UserExistError(Exception):
    def __init__(self):
        self.code = 6
        self.name = "UserExistError"
        self.desc = "User with such values already exists"


class IncorrectValueError(Exception):
    def __init__(self):
        self.code = 7
        self.name = "IncorrectValueError"
        self.desc = "Try to input correct values"


class TitleError(Exception):
    def __init__(self):
        self.code = 8
        self.name = "TitleError"
        self.desc = "Task with such title doesn't exist"


class IncorrectDateValueError(Exception):
    def __init__(self):
        self.code = 9
        self.name = "IncorrectDateValueError"
        self.desc = "Try to input date in format (%d/%m/%y %H:%M)"


class UserNotExistError(Exception):
    def __init__(self):
        self.code = 10
        self.name = "UserNotExistError"
        self.desc = "User with such login doesn't exists"


class CronValueError(Exception):
    def __init__(self):
        self.code = 11
        self.name = "CronValueError"
        self.desc = """Try to input period in cron format like
           ┌───────────── minute (0 - 59)
#          │ ┌───────────── hour (0 - 23)
#          │ │ ┌───────────── day of month (1 - 31)
#          │ │ │ ┌───────────── month (1 - 12)
#          │ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday;
#          │ │ │ │ │                                       7 is also Sunday on some systems)
#          │ │ │ │ │
#          │ │ │ │ │
#          * * * * *  command to execute"""


class TagError(Exception):
    def __init__(self):
        self.code = 12
        self.name = "TagError"
        self.desc = "No tasks with such tag"

