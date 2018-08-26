class ArgvHandler(object):
    def __init__(self, sys_args):
        self.sys_args = sys_args

    def help_msg(self, error_msg=''):
        """打印帮助"""
        msgs = """
        %s 
        run 启动交互程序
        """ % (error_msg)
        exit(msgs)

    def call(self):
        """根据用户参数，调用不同的方法"""
        if len(self.sys_args) == 1:
            self.help_msg()

        if hasattr(self, self.sys_args[1]):
            func = getattr(self, self.sys_args[1])
            func()
        else:
            self.help_msg('没有这个方法：%s' % self.sys_args[1])

    def run(self):
        """启动用户交互页面"""
        from backend.ssh_interactive import SshHandler
        obj = SshHandler(self)
        obj.interactive()