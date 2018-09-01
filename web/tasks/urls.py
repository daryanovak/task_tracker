from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('<int:task_id>/delete', views.delete, name='delete'),
    path('<int:task_id>/parent', views.create_subtask, name='parent'),
    path('<int:task_id>/edit', views.edit, name='edit'),
    path('<int:task_id>/', views.detail, name='detail'),
    path('<int:task_id>/comment', views.comment, name='comment'),
    path('<int:task_id>/share_permission', views.share_permission, name='share_permission'),
    path('<int:task_id>/delete_permission', views.delete_permission, name='delete_permission'),
    path('<int:task_id>/toggle_task_completion', views.toggle_task_completion, name='toggle_task_completion')

]