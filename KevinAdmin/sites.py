from KevinAdmin.admin_base import BaseKevinAdmin


class AdminSite(BaseKevinAdmin):
    def __init__(self):
        self.enabled_admins = {}

    def register(self, model_class, admin_class=None):
        # admin.site.register(User,UserAdmin)
        app_name = model_class._meta.app_label  # 根据model获取app名字
        table_name = model_class._meta.model_name  # 传入的model_class是个对象
        if not admin_class:
            admin_class = BaseKevinAdmin()
        else:
            admin_class = admin_class()
        admin_class.model = model_class
        if app_name not in self.enabled_admins:
            self.enabled_admins[app_name] = {}
        self.enabled_admins[app_name][table_name] = admin_class


site = AdminSite()