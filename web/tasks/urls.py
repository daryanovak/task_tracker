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
]