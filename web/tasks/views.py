from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from tracker_lib.controllers.task import TaskController

from tasks.forms import TaskForm


@login_required
def index(request):
    current_user = request.user
    controller = TaskController(current_user.id)
    tasks = controller.get_tasks()
    return render(request, 'tasks/tasks-list.html', {'tasks': tasks})


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
            controller.create_task(form.cleaned_data['title'], form.cleaned_data['text'], form.cleaned_data['status'])
            return HttpResponseRedirect('/tasks')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TaskForm()

    return render(request, 'tasks/task-create.html', {'form': form})