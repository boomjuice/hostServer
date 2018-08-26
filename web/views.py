from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json

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


def batch_cmd_control(request):
    if request.method == 'POST':
        task_arguments = json.loads(request.POST.get('task_arguments'))
        print(task_arguments)
    return render(request, 'host_control.html')
