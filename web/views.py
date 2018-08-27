from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from backend.BatchTask import BatchTaskHandler
from web.models import *


# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')


def acc_login(request):
    error_msg = ''
    if request.method == 'POST':
        print(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', '/'))
        else:
            error_msg = 'Wrong username or password'
    return render(request, 'login.html', {'error_msg': error_msg})


def acc_logout(request):
    logout(request)
    return redirect('/login/')


@login_required()
def web_ssh(request):
    return render(request, 'web_ssh.html')


@login_required()
def batch_cmd_control(request):
    return render(request, 'host_control.html')


@login_required()
def batch_file_transfer(request):
    return render(request, 'file_transfer.html')


def batch_task_mgr(request):
    task_obj = BatchTaskHandler(request)
    response = {
        'task_id': task_obj.task_obj.id,
        'selected_hosts': list(task_obj.task_obj.tasklogdetail_set.all()
                               .values('id', 'host_to_remote_user__host__ip_address',
                                       'host_to_remote_user__host__name',
                                       'host_to_remote_user__remote_user__username')
                               )
    }

    return HttpResponse(json.dumps(response))


def get_task_result(request):
    task_id = request.GET.get('task_id')
    task_obj = list(TaskLogDetail.objects.filter(task_id=task_id).values('id', 'status', 'result'))

    return HttpResponse(json.dumps(task_obj))


@login_required()
def tasks_log(request):
    return render(request, 'task_log_detail.html')
