from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from tracker_lib.controllers.task import TaskController
from tracker_lib.controllers.comment import CommentController
from tracker_lib.enums import Status

from tasks.forms import TaskForm


@login_required
def index(request):
    current_user = request.user

    controller = TaskController(current_user.id)
    tasks = controller.get_tasks()

    tags = set()
    for task in tasks:
        if task['tags']:
            tags.update(map(lambda tag: tag.strip(), task['tags'].split(',')))

    if request.is_ajax():
        active_tag = request.GET.get('active_tag')
        if active_tag:
            if active_tag != 'all':
                tasks = controller.get_tasks_by_tag(active_tag)
            return render(request, 'tasks/tasks-list.html', {'tasks': tasks, 'tags': tags})
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
            controller.create_task(data['title'], data['text'], data['status'], tags=data['tags'])
            return HttpResponseRedirect('/tasks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TaskForm()

    return render(request, 'tasks/task-create.html', {'form': form})


def create_subtask(request, task_id):
    current_user = request.user
    print(task_id)
    controller = TaskController(current_user.id)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TaskForm(request.POST)
        # check whether it's valid:

        if form.is_valid():
            data = form.cleaned_data
            controller.create_task(title=data['title'], text=data['text'], status=data['status'], parent_id=task_id,
                                   tags=data['tags'])
            return HttpResponseRedirect('/tasks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TaskForm()

    return render(request, 'tasks/task-create.html', {'form': form})


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
    print(task)

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


