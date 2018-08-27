from .models import *
from KevinAdmin.admin_base import BaseKevinAdmin
from KevinAdmin.sites import site


class TaskLogAdmin(BaseKevinAdmin):
    list_display = ['id', 'status', 'host_to_remote_user', 'date']
    list_filter = ['status', 'host_to_remote_user', ]


class UserAdmin(BaseKevinAdmin):
    list_display = ['id', 'email', 'name']


site.register(UserProfile)
site.register(AuditLog)
site.register(TaskLogDetail, TaskLogAdmin)
site.register(Tasks)
site.register(Host)
site.register(HostToRemoteUser)
site.register(RemoteUser)
site.register(HostGroup)
site.register(IDC)
