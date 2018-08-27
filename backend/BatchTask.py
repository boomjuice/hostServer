from web.models import *
import json
from django.conf import settings
import subprocess


class BatchTaskHandler(object):
    def __init__(self, request):
        self.request = request
        self.run_task()

    def task_parser(self):
        """解析任务"""
        self.task_arguments = json.loads(self.request.POST.get('task_arguments'))
        task_type = self.task_arguments.get('task_type')

        if hasattr(self, task_type):
            task_func = getattr(self, task_type)
            task_func()
        else:
            print('cannot find task', task_type)

    def run_task(self):
        """调用任务"""
        self.task_parser()

    def cmd(self):
        """批量命令
        1. 生成任务在数据库的记录，拿到任务id
        2. 触发任务，不阻塞
        3.返回任务id给前端
        """
        task_obj = Tasks.objects.create(
            task_type='cmd',
            content=self.task_arguments.get('cmd'),
            user=self.request.user,
        )
        selected_hosts = set(self.task_arguments.get('selected_hosts'))
        task_obj_list = []
        for id in selected_hosts:
            task_obj_list.append(
                TaskLogDetail(task=task_obj, host_to_remote_user_id=id, result='init...')
            )
        TaskLogDetail.objects.bulk_create(task_obj_list)
        task_script = "python %s/backend/task_runner.py %s" % (settings.BASE_DIR, task_obj.id)

        cmd_process = subprocess.Popen(task_script, shell=True)

        print("running batch commands....")

        self.task_obj = task_obj
