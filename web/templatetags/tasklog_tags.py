from django.template import Library
from web.models import *

register = Library()


@register.simple_tag()
def get_task_count(user):
    task_count = 0
    for task in user.tasks_set.all():
        task_count += task.tasklogdetail_set.count()
    return task_count


@register.simple_tag()
def get_succeed_task(user):
    succeed_count = 0
    for task in user.tasks_set.all():
        succeed_count += task.tasklogdetail_set.filter(status=1).count()
    return succeed_count


@register.simple_tag()
def get_failed_task(user):
    failed_count = 0
    for task in user.tasks_set.all():
        failed_count += task.tasklogdetail_set.filter(status=2).count()
    return failed_count
