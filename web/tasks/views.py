from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from tracker_lib.controllers.task import TaskController
from tracker_lib.controllers.comment import CommentController
from tracker_lib.enums import TaskStatus

from tasks.forms import TaskForm


periods = {
    'current_day': (datetime.today(), datetime.today(),),
    'tomorrow': (datetime.today(), (datetime.today() + timedelta(days=1))),
    'next_week': (datetime.today(), (datetime.today() + timedelta(weeks=1)))
}


@login_required
def index(request):
    current_user = request.user

    controller = TaskController(current_user.id)
    tasks = controller.get_tasks()

    tags = set()
    for task in tasks:
        if task['tags']:
            tags.update(map(lambda tag: tag.strip(), task['tags'].split(',')))

    for task in tasks:
        task['subtasks'] = controller.get_task_subtasks(task['id'])

    if request.is_ajax():
        active_tag = request.GET.get('active_tag')
        req_period = request.GET.get('period')
        if active_tag:
            if active_tag != 'all':
                tasks = controller.get_tasks_by_tag(active_tag)
            return render(request, 'tasks/tasks-list.html', {'tasks': tasks, 'tags': tags})
        if req_period:
            res_tasks = []
            result_tasks = []
            date_tasks_list = controller.get_tasks_on_period(periods[req_period][0].strftime('%d/%m/%y'), periods[req_period][1].strftime('%d/%m/%y'))

            #get all tasks
            for date_tasks in date_tasks_list:
                date = list(date_tasks.keys())[0]
                for task in date_tasks[date]:
                    res_tasks.append(task)

            #remove duplicate
            for res_task in res_tasks:
                is_dublicate = False
                for res in result_tasks:
                    if res_task['id'] == res['id']:
                        is_dublicate = True

                if not is_dublicate:
                    result_tasks.append(res_task)
                else:
                    is_dublicate = False

            for task in result_tasks:
                task['subtasks'] = controller.get_task_subtasks(task['id'])

            return render(request, 'tasks/tasks-list.html', {'tasks': result_tasks, 'tags': tags})

    return render(request, 'tasks/index.html', {'tasks': tasks, 'tags': tags})


@login_required
def create(request):
    current_user = request.user

    controller = TaskController(current_user.id)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TaskForm(request.POST)
        # check whether it's valid:

        if form.is_valid():
            data = form.cleaned_data
            if data['period'] and data['start_date']:
                controller.create_periodic_task(
                    data['title'],
                    data['text'],
                    data['status'],
                    tags=data['tags'],
                    start_date=data['start_date'].strftime('%d/%m/%y %H:%M') if data['start_date'] else None,
                    deadline=data['date'].strftime('%d/%m/%y %H:%M') if data['date'] else None,
                    period=data['period']
                )
            else:
                controller.create_task(
                    data['title'],
                    data['text'],
                    data['status'],
                    tags=data['tags'],
                    date=data['date'].strftime('%d/%m/%y %H:%M') if data['date'] else None,
                )
            return HttpResponseRedirect('/tasks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TaskForm()

    return render(request, 'tasks/task-create.html', {'form': form})


@login_required
def create_subtask(request, task_id):
    current_user = request.user
    controller = TaskController(current_user.id)

    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            if data['period'] and data['start_date']:
                controller.create_periodic_task(
                    data['title'],
                    data['text'],
                    data['status'],
                    tags=data['tags'],
                    start_date=data['start_date'].strftime('%d/%m/%y %H:%M') if data['start_date'] else None,
                    deadline=data['date'].strftime('%d/%m/%y %H:%M') if data['date'] else None,
                    period=data['period'],
                    parent_id=task_id
                )
            else:
                controller.create_task(
                    data['title'],
                    data['text'],
                    data['status'],
                    tags=data['tags'],
                    date=data['date'].strftime('%d/%m/%y %H:%M') if data['date'] else None,
                    parent_id=task_id
                )
            return HttpResponseRedirect('/tasks')

    else:
        form = TaskForm()

    return render(request, 'tasks/create-subtask.html', {'form': form, 'task_id': task_id})


@csrf_exempt
@login_required
def delete(request, task_id):
    # if this is a POST request we need to process the form data
    current_user = request.user

    controller = TaskController(current_user.id)
    controller.delete_task(task_id=task_id)
    return HttpResponseRedirect(redirect_to='/tasks')


@login_required
def edit(request, task_id):
    # if this is a POST request we need to process the form data

    current_user = request.user
    controller = TaskController(current_user.id)
    task = controller.get_task_by_id(task_id)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TaskForm(request.POST)
        # check whether it's valid:

        if form.is_valid():
            data = form.cleaned_data
            controller.edit_task(task_id,
                                 {
                                     'title': data['title'],
                                     'text': data['text'],
                                     'status': data['status'],
                                     'tags': data['tags']
                                 })
            return HttpResponseRedirect('/tasks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TaskForm(data=task)

    return render(request, 'tasks/edit-task.html', {'form': form, 'task': task})


@login_required
def detail(request, task_id):

    current_user = request.user

    controller = TaskController(current_user.id)
    comment_controller = CommentController(current_user.id)

    task = controller.get_task_by_id(task_id=task_id)
    comment_list = comment_controller.get_task_comments(task_id=task_id)
    user_list = []
    for user in task['users']:
        user_list.append(User.objects.get(id=user))

    # user_pk_list = SharedTask.objects.filter(task=task).values_list('user', flat=True)
    # user_list = User.objects.filter(id__in=user_pk_list)
    owner = task['creator']
    try:
        owner = User.objects.get(id=owner)
    except:
        raise Exception()
    print(owner)
    return render(request, 'tasks/detail.html', {'task': task, 'comment_list': comment_list, 'user_list': user_list,
                                                 'owner': owner})


@login_required
def comment(request, task_id):
    current_user = request.user

    controller = TaskController(current_user.id)
    comment_controller = CommentController(current_user.id)

    controller.get_task_by_id(task_id=task_id)
    comment = comment_controller.create_task_comment(task_id=task_id, text=request.POST.get('text'))
    return HttpResponseRedirect('/tasks/{}/'.format(task_id))


@login_required
def share_permission(request, task_id):
    current_user = request.user
    try:
        user = User.objects.get(username=request.POST.get('user'))
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'User not found',
            'url': '/tasks/{}/'.format(task_id),
        })

    controller = TaskController(current_user.id)
    controller.share_permission(new_user_id=user.id, task_id=task_id)
    return JsonResponse({
        'success': True,
        'url': '/tasks/{}/'.format(task_id),
    })


@login_required
def delete_permission(request, task_id):
    current_user = request.user
    controller = TaskController(current_user.id)
    controller.delete_permission(task_id, int(request.POST.get('user_id')))
    return JsonResponse({
        'success': True,
        'url': request.POST.get('redirect')
    })


@login_required
def toggle_task_completion(request, task_id):
    current_user = request.user
    controller = TaskController(current_user.id)
    task = controller.get_task_by_id(task_id)

    if task['status'] == TaskStatus.PLANNED.value:
        new_status = TaskStatus.COMPLETED.value
    else:
        new_status = TaskStatus.PLANNED.value
    controller.edit_task(task_id=task_id, edited_task={'status': str(new_status) })
    return JsonResponse({'success': True})
