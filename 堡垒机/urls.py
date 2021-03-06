"""堡垒机 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from web import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.acc_login, name='acc_login'),
    url(r'^logout/$', views.acc_logout, name='acc_logout'),
    url(r'^kevin-admin/', include('KevinAdmin.urls')),
    url(r'^web-ssh/$', views.web_ssh, name='web_ssh'),
    url(r'^batch-task-mgr/$', views.batch_task_mgr, name='batch_task_mgr'),
    url(r'^batch-file-transfer/$', views.batch_file_transfer, name='batch_file_transfer'),
    url(r'^get-task-result/$', views.get_task_result, name='get_task_result'),
    url(r'^batch-cmd-control/$', views.batch_cmd_control, name='batch_cmd_control'),
    url(r'^tasks-log/$', views.tasks_log, name='tasks_log'),

]
