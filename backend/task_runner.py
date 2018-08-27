import sys, os
from concurrent.futures import ThreadPoolExecutor
import paramiko
import datetime

def ssh_cmd(sub_task_obj):
    print("start therad ", sub_task_obj)
    host_to_user_obj = sub_task_obj.host_to_remote_user
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=host_to_user_obj.host.ip_address,
                    port=host_to_user_obj.host.port,
                    username=host_to_user_obj.remote_user.username,
                    password=host_to_user_obj.remote_user.password,
                    timeout=5)
        stdin, stdout, stderr = ssh.exec_command(sub_task_obj.task.content)
        stdout_res = stdout.read()
        stderr_res = stderr.read()
        sub_task_obj.result = stdout_res + stderr_res
        if stderr_res:
            sub_task_obj.status = 2
        else:
            sub_task_obj.status = 1
    except Exception as e:
        sub_task_obj.result = e
        sub_task_obj.status = 2
    sub_task_obj.date = datetime.datetime.now()
    sub_task_obj.save()
    ssh.close()


def file_transfer(sub_task_obj, task_arguments):
    print("start therad ", sub_task_obj)
    host_to_user_obj = sub_task_obj.host_to_remote_user
    ip_address = host_to_user_obj.host.ip_address
    username = host_to_user_obj.remote_user.username
    password = host_to_user_obj.remote_user.password
    port = host_to_user_obj.host.port
    try:
        t = paramiko.Transport((ip_address, port))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        if task_arguments['file_transfer_type'] == 'send':
            file_name = task_arguments['local_file_path'].rsplit('/')[1]
            remote_file_path = task_arguments['remote_file_path'] + file_name
            sftp.put(task_arguments['local_file_path'], remote_file_path)
            result = "file [%s] sends to [%s] succeed!" % (
                task_arguments["local_file_path"], remote_file_path)
        else:
            download_dir = conf.settings.DOWNLOAD_DIR
            local_download_dir = download_dir + '/%s' % task_obj.id
            print(local_download_dir)
            if not os.path.isdir(local_download_dir):
                os.mkdir(local_download_dir)
            origin_file_name = task_arguments['remote_file_path'].split('/')[-1]
            file_name = '(%s)%s' % (ip_address, origin_file_name)
            local_file_path = local_download_dir + task_arguments['local_file_path'] + '/' + file_name
            sftp.get(task_arguments['remote_file_path'], local_file_path)
            result = "download remote [%s]  to [%s] succeed" % (task_arguments['remote_file_path'], local_file_path)
        t.close()
        sub_task_obj.status = 1
    except Exception as e:
        result = e
        sub_task_obj.status = 2
    sub_task_obj.date = datetime.datetime.now()
    sub_task_obj.result = result
    sub_task_obj.save()


if __name__ == '__main__':

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(base_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "堡垒机.settings")
    import django, json

    django.setup()
    from django import conf
    from web.models import *

    if (len(sys.argv)) == 1:
        exit("task id not provided!")
    task_id = sys.argv[1]
    task_obj = Tasks.objects.get(id=task_id)
    print("task runner..", task_obj)

    pool = ThreadPoolExecutor(10)

    if task_obj.task_type == 'cmd':
        for sub_task_obj in task_obj.tasklogdetail_set.all():
            pool.submit(ssh_cmd, sub_task_obj)
    else:
        task_arguments = json.loads(task_obj.content)
        for sub_task_obj in task_obj.tasklogdetail_set.all():
            pool.submit(file_transfer, sub_task_obj, task_arguments)
    pool.shutdown(wait=True)
