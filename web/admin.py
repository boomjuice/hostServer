from django.contrib import admin
from web.models import *
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(HostToRemoteUser)
admin.site.register(Host)
admin.site.register(HostGroup)
admin.site.register(IDC)
admin.site.register(RemoteUser)
admin.site.register(AuditLog)
admin.site.register(Tasks)
admin.site.register(TaskLogDetail)