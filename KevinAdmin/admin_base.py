from django.shortcuts import render


class BaseKevinAdmin(object):
    def __init__(self):
        if not self.actions:
            self.actions.extend(self.default_actions)

    list_display = []
    list_filter = []
    search_field = []
    readonly_fields = []
    filter_horizontal = []
    list_per_page = 10
    actions = []
    default_actions = ['delete_selected_obj',]

    def delete_selected_obj(self, request, queryset):
        # 修改删除页面成为共用页面
        queryset_list = queryset
        id_list = [i.id for i in queryset_list]

        return render(request, 'kevinadmin/table_obj_delete.html',
                      {'admin_class': self, 'queryset_list': queryset_list, 'id_list': id_list})
