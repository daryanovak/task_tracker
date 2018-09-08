from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('delete/<int:task_id>', views.delete, name='delete'),
    path('parent/<int:task_id>', views.create_subtask, name='parent'),
    path('edit/<int:task_id>', views.edit, name='edit'),
    path('<int:task_id>/', views.detail, name='detail'),
    path('comment/<int:task_id>', views.comment, name='comment'),
    path('share_permission/<int:task_id>', views.share_permission, name='share_permission'),
    path('delete_permission/<int:task_id>', views.delete_permission, name='delete_permission'),
    path('toggle_task_completion/<int:task_id>', views.toggle_task_completion, name='toggle_task_completion')

]