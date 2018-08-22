# periodic_task= [{'title': periodic_task.title, 'text': periodic_task.text, 'status': periodic_task.status,
#                       'tags': periodic_task.tags, 'start_date': periodic_task.start_date,
#                       'period': periodic_task.period, 'date': periodic_task.date, 'parent_id': periodic_task.parent_id, 'creator': periodic_task.creator}]

# task = [{'title': task.title, 'text': task.text, 'status': task.status, 'tags': task.tags, 'date': task.date,
#              'parent_id': task.parent_id, 'periodic_task_id': periodic_task_id, 'creator':task.creator}]


def print_task(task):
    t = task['type']
    if task['type'] == "PeriodicTask":
        print(str(task['id']) + "--id--" + " " + task['title'] + " " + task['text'] + " " + str(task['status'])
              + " " + "---start---" + " " + str(task['start_date']) +" " + "---end_date--"  + str(task['date']) )

    if task['type'] == "Task":
        print(str(task['id']) + "--id--" + " " + task['title'] + " " + task['text'] + " "
              + str(task['status']))

