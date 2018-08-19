import lib.storage.task as task_storage
import lib.storage.user as user_storage
from lib.models import Task, PeriodicTask
import lib.storage.comment as comment_storage
from datetime import datetime, timedelta
from lib.enums import Parameters
from lib.enums import Status
import pickle
from lib.helpers.cron_period_helper import CronPeriodHelper
import typing


class TaskController():
    def __init__(self):
        self.cph = CronPeriodHelper

    def create_task(self, title, text, status, tags="", parent_id=None, date=None):
        current_user_id = user_storage.get_current_user()
        if parent_id:
            pass
        else:
            parent_id = None

        if date:
            date_object = datetime.strptime(date, '%d/%m/%y %H:%M')
        else:
            date_object = None

        return task_storage.add_task(user_id=current_user_id, title=title, text=text, status=status, tags=tags, parent_id=parent_id, date=date_object)

    def create_periodic_task(self, title, text, status, start_date, date, period, tags=None, parent_id=None):
        current_user_id = user_storage.get_current_user()
        if parent_id:
            pass
        else:
            parent_id = None

        if date:
            date_object = datetime.strptime(date, '%d/%m/%y %H:%M')
        else:
            date_object = None

        if start_date:
            start_date_object = datetime.strptime(start_date, '%d/%m/%y %H:%M')
        else:
            start_date_object = None

        task_storage.add_periodic_task(user_id=current_user_id, title=title, text=text, status=status,
                                       start_date=start_date_object, date=date_object, period=period, tags=tags,
                                       parent_id=parent_id)

    def get_task_by_id(self, task_id):
        current_user_id = user_storage.get_current_user()
        return task_storage.get_task_by_id(task_id=task_id, user_id=current_user_id)

    def show_my_tasks(self):
        current_user_id = user_storage.get_current_user()
        return task_storage.get_tasks(user_id=current_user_id)

    def delete_task(self, task_id):
        current_user_id = user_storage.get_current_user()
        task_storage.delete_task(user_id=current_user_id, task_id=task_id)

    def edit_task_title(self, task_id, new_title):
        current_user_id = user_storage.get_current_user()
        task_storage.edit_task(user_id=current_user_id, task_id=task_id, enum_parameter_value=Parameters.TITLE,
                               modified_parameter=new_title)

    def edit_task_text(self, task_id, new_text):
        current_user_id = user_storage.get_current_user()
        task_storage.edit_task(user_id=current_user_id, task_id=task_id, enum_parameter_value=Parameters.TEXT,
                               modified_parameter=new_text)

    def edit_task_status(self, task_id, new_status):
        current_user_id = user_storage.get_current_user()
        new_status = int(new_status)
        values = [item.value for item in Status]
        if new_status in values:
            task_storage.edit_task(user_id=current_user_id, task_id=task_id, enum_parameter_value=Parameters.STATUS,
                               modified_parameter=new_status)
        else:
            raise Exception("Dashaaa its status")

    def get_subtasks_of_task(self, task_id):
        current_user_id = user_storage.get_current_user()
        return task_storage.get_subtask_of_task(user_id=current_user_id, task_id=task_id)

    def share_permission(self, new_user_id, task_id):
        current_user_id = user_storage.get_current_user()
        task_storage.share_permission(my_user_id=current_user_id, task_id=task_id, new_user_id=new_user_id)

    def get_task_by_tag(self, tag):
        current_user_id = user_storage.get_current_user()
        return task_storage.get_tasks_by_type_of_parameter(user_id=current_user_id, parameter=Parameters.TAGS, parametr_value=tag)

    def get_tasks_on_period(self, start, end):
        current_user_id = user_storage.get_current_user()
        # start = datetime.strptime(start, '%d/%m/%y %H:%M')
        # end = datetime.strptime(end, '%d/%m/%y %H:%M')
        # current_user_id = user_storage.get_current_user()

        """
         Returns the tasks by datetime period
        :param start: start date in datetime format d%/m%/y% 00:00
        :param end: end date in datetime format d%/m%/y% 00:00
        :return: dict
        """
        cph = CronPeriodHelper()
        start_date = datetime.strptime(start, '%d/%m/%y')
        end_date = datetime.strptime(end, '%d/%m/%y')
        tasks = task_storage.get_tasks(current_user_id)
        task_date_comments_dict = dict()
        current_user_id = user_storage.get_current_user()
        response = []

        # if type(start) != datetime or type(end) != datetime:
        # response = {}
        #     raise errs.IncorrectDateValueError()

        # for task in tasks:
        #     if isinstance(task, PeriodicTask):
        #         dates = cph.get_tasks_periods(start_date, end_date,
        #                                       task.period)
        #         dates_dict = dict()
        #         for date in dates:
        #             dates_dict[date] = comment_storage.get_comments_of_task(current_user_id, task.id)
        #         task_date_comments_dict[task] = {'dates': dates_dict}

        temp_date = start_date
        for i in range(int((end_date - start_date).days) + 1):
            tasks_list = list()
            for task in tasks:
                if isinstance(task, PeriodicTask):
                    if cph.in_period(task.period, temp_date):
                        tasks_list.append(task)
                else:
                    if temp_date == task.date:
                        if task.periodic_task_id:
                            tasks_list = list(filter(lambda task: task.id == task.periodic_task_id, tasks_list))
                        tasks_list.append(task)
            if len(tasks_list) > 0:
                response.append({temp_date: tasks_list})
            temp_date = temp_date + timedelta(days=1)

        # temp_date = start_date
        #
        #
        # is_printable = False
        # for i in range(int((end_date - start_date).days) + 1):
        #     tasks_to_print = dict()
        #
        #     for task in task_date_comments_dict:
        #         if temp_date.date().__str__() in task_date_comments_dict[task]['dates']:
        #             is_printable = True
        #             tasks_to_print[task] = task_date_comments_dict[task]
        #
        #     if is_printable:
        #         response[temp_date] = tasks_to_print
        #         # print(temp_date.date().__str__() + ':')
        #         # print('tasks:')
        #         # for task in tasks_to_print:
        #         #     print(task)
        #         #     for comment in tasks_to_print[task]['dates'][temp_date.date().__str__()]:
        #         #         print('comments:')
        #         #         print('-' + comment.__str__())
        #
        #     is_printable = False
        #
        #     temp_date = temp_date + timedelta(days=1)

        return response



