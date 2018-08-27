from django.contrib import admin
from web.models import *


# Register your models here.
class TaskLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'host_to_remote_user', 'date']


admin.site.register(UserProfile)
admin.site.register(HostToRemoteUser)
admin.site.register(Host)
admin.site.register(HostGroup)
admin.site.register(IDC)
admin.site.register(RemoteUser)
admin.site.register(AuditLog)
admin.site.register(Tasks)
admin.site.register(TaskLogDetail, TaskLogAdmin)
