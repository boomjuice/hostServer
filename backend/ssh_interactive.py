from django.contrib.auth import authenticate
from web import models
from backend import paramiko_ssh


class SshHandler(object):
    """堡垒机交互脚本"""

    def __init__(self, argv_handler_instance):
        self.models = models
        self.argv_handler_instance = argv_handler_instance

    def auth(self):
        """认证系统"""
        count = 0
        while count < 3:
            username = input('堡垒机账号：').strip()
            password = input('password：').strip()
            user = authenticate(username=username, password=password)
            if user:
                self.user = user
                return True
            else:
                count += 1
                print('账号或密码错误，当前是第%s次，三次失败后退出程序' % count)

    def interactive(self):
        """启动交互脚本"""
        if self.auth():
            print('The following HostList which you can access')
            while True:
                host_group_list = self.user.host_groups.all()
                for index, host_group_obj in enumerate(host_group_list):
                    print('%s.\t%s[%s]' % (index, host_group_obj.name, host_group_obj.host_to_remote_users.count()))
                print('z. \t未分组的主机[%s]' % self.user.host_to_remote_users.count())

                choice = input('请输入主机组>>：').strip()
                if choice.isdigit():
                    choice = int(choice)
                    selected_host_obj = host_group_list[choice]
                elif choice == 'z':
                    selected_host_obj = self.user

                while True:
                    for index, host_to_user_obj in enumerate(selected_host_obj.host_to_remote_users.all()):
                        print('%s .\t %s' % (index, host_to_user_obj))
                    choice = input("请选择主机>>:").strip()
                    if choice.isdigit():
                        choice = int(choice)
                        selected_host_to_user_obj = selected_host_obj.host_to_remote_users.all()[choice]
                        print("going to logon  %s" % selected_host_to_user_obj)
                        paramiko_ssh.ssh_connect(self, selected_host_to_user_obj)

                    if choice == 'b':
                        break



