from enum import Enum


class TaskParameters(Enum):
    TITLE = 1
    TEXT = 2
    STATUS = 3
    TAGS = 4
    PARENT_ID = 5


class TaskStatus(Enum):
    PLANNED = 0
    COMPLETED = 1
    FAILED = 2
