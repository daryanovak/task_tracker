import lib.storage.task as task_storage
import lib.storage.user as user_storage
from datetime import datetime
from lib.enums import Parameters


class TaskController():
    def create_task(self, title, text, status, tags, parent_title, date):
        current_user_id = user_storage.get_current_user()
        if parent_title:
            parent_id = task_storage.get_task_id_by_title(title=parent_title)
        else:
            parent_id = None

        if date:
            date_object = datetime.strptime(date, '%d/%m/%y %H:%M')
            print(type(date_object))
        else:
            date_object = None

        task_storage.add_task(user_id=current_user_id, title=title, text=text, status=status, tags=tags, parent_id=parent_id, date=date_object)

    def create_periodic_task(self, title, text, status, start_date, date, period, tags, parent_title):
        current_user_id = user_storage.get_current_user()
        if parent_title:
            parent_id = task_storage.get_task_id_by_title(title=parent_title)
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

        task_storage.add_periodic_task(user_id=current_user_id, title=title, text=text, status=status,start_date=start_date_object,
                                       date=date_object, period=period, tags=tags, parent_id=parent_id)

    def get_task_by_title(self, title):
        return task_storage.get_task_by_type_of_parameter(Parameters.TITLE, title)

    def delete_task_by_title(self, title):
        task_id = task_storage.get_task_id_by_title(title=title)
        task_storage.delete_task_by_title(user_id=None, task_id=task_id)#task_id

    def edit_task_title(self, title, new_title):
        task_id = task_storage.get_task_id_by_title(title=title)
        task_storage.edit_task(user_id=None, task_id=task_id, enum_parameter_value=Parameters.TITLE,
                               modified_parameter=new_title)

    def edit_task_text(self, title, new_text):
        task_id = task_storage.get_task_id_by_title(title=title)
        task_storage.edit_task(user_id=None, task_id=task_id, enum_parameter_value=Parameters.TEXT,
                               modified_parameter=new_text)

    def edit_task_status(self, title, new_status):
        task_id = task_storage.get_task_id_by_title(title=title)
        task_storage.edit_task(user_id=None, task_id=task_id, enum_parameter_value=Parameters.STATUS,
                               modified_parameter=new_status)

    def get_subtasks_of_task(self, title):
        task_id = task_storage.get_task_id_by_title(title=title)
        task_storage.get_subtask_of_task(user_id=None, task_id=task_id)

    def share_permission(self, user_login, title):
        task_id = task_storage.get_task_id_by_title(title=title)
        new_user_id = task_storage.get_user_id_by_login(login=user_login)
        task_storage.share_permission(my_user_id=None, title_id= task_id, new_user_id=new_user_id)

    def get_task_by_tag(self, tag):
        return task_storage.get_task_by_type_of_parameter(parameter=Parameters.TAGS, parameter_value=tag)



