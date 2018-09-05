from django import template
from django.contrib.auth.models import User
from tracker_lib.enums import TaskStatus

register = template.Library()


@register.filter
def get_user(user_id):
    return User.objects.get(id=user_id)


@register.filter
def get_status(status):
    return TaskStatus(status).name


