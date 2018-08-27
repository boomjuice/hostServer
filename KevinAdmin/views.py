from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from KevinAdmin.app_setup import kevinadmin_auto_discover
from KevinAdmin.sites import site
from KevinAdmin.util.Pager import Pagination
from django.db.models import Q
from KevinAdmin.kevin_form import create_dynamic_model_form
import json
from KevinAdmin.permissions import check_permission

kevinadmin_auto_discover()


@login_required
def app_index(request):
    return render(request, 'kevinadmin/app_index.html', {'site': site})


@login_required()
def app_single(request, single_name):
    return render(request, 'kevinadmin/app_index.html', {'site': site, 'single_name': single_name})


def get_filter_result(request, queryset):
    """处理过滤条件，根据条件筛选数据"""
    filter_conditions = {}
    for k, v in request.GET.items():
        if k in ('_p', '_o', '_q'): continue
        if v:
            if k == 'date':
                date = v.split(' ', 1)[0]
                filter_conditions['date__gte'] = date
            else:
                filter_conditions[k] = v

    return queryset.filter(**filter_conditions), filter_conditions


def get_orderby_result(request, queryset, admin_class):
    order_conditions = {}
    order_index = request.GET.get('_o')
    if order_index:
        order_key = admin_class.list_display[abs(int(order_index))]  # index 所对应的 列名
        order_conditions[order_key] = order_index
        if order_index.startswith('-'):
            order_key = '-' + order_key
        return queryset.order_by(order_key), order_conditions
    else:
        return queryset, order_conditions


def get_search_result(request, queryset, admin_class):
    search_condition = request.GET.get('_q', '')
    if search_condition:
        q = Q()
        q.connector = 'OR'
        for search_field in admin_class.search_fields:
            q.children.append(("%s__contains" % search_field, search_condition))

        return queryset.filter(q), search_condition
    else:
        return queryset, search_condition


@login_required
def table_obj_list(request, app_name, table_name):
    admin_class = site.enabled_admins[app_name][table_name]
    if request.method == 'POST':
        selected_action = request.POST.get('action')
        id_list = json.loads(request.POST.get('id_list'))
        if selected_action:  # 如果有 则表示请求批量删除页面 如果没有则是确认默认删除
            selected_objs = admin_class.model.objects.filter(id__in=id_list)
            admin_action_func = getattr(admin_class, selected_action)
            return admin_action_func(request, selected_objs)
        else:
            if id_list:
                admin_class.model.objects.filter(id__in=id_list).delete()

    queryset = admin_class.model.objects.all().order_by('-id')

    queryset, filter_conditions = get_filter_result(request, queryset)  # 处理过滤条件
    admin_class.filter_conditions = filter_conditions

    queryset, order_conditions = get_orderby_result(request, queryset, admin_class)  # 升降序处理

    queryset, search_condition = get_search_result(request, queryset, admin_class)
    admin_class.search_condition = search_condition

    count = queryset.count()
    pagination = Pagination(count, request.GET.get('_p'), admin_class.list_per_page, 5)
    queryset = queryset[pagination.start():pagination.end()]
    page_str = pagination.page_str(filter_conditions, order_conditions, search_condition)
    # 将过滤条件，排序条件传入分页器中，在url上添加get条件
    return render(request, 'kevinadmin/table_obj_list.html', locals())


@login_required
def table_obj_change(request, app_name, table_name, obj_id):
    admin_class = site.enabled_admins[app_name][table_name]
    model_form = create_dynamic_model_form(admin_class)
    obj = admin_class.model.objects.get(id=obj_id)
    if request.method == 'GET':
        form_obj = model_form(instance=obj)
    elif request.method == 'POST':
        form_obj = model_form(instance=obj, data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('/kevin-admin/%s/%s' % (app_name, table_name))
    return render(request, 'kevinadmin/table_obj_change.html', locals())


@login_required
def table_obj_add(request, app_name, table_name):
    admin_class = site.enabled_admins[app_name][table_name]
    model_form = create_dynamic_model_form(admin_class, form_add=True)
    if request.method == 'GET':
        form_obj = model_form()
    elif request.method == 'POST':
        form_obj = model_form(data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('/kevin-admin/%s/%s' % (app_name, table_name))
    return render(request, 'kevinadmin/table_obj_add.html', locals())


@login_required
def table_obj_delete(request, app_name, table_name, obj_id):
    admin_class = site.enabled_admins[app_name][table_name]
    obj = admin_class.model.objects.get(id=obj_id)
    if request.method == 'POST':
        obj.delete()
        return redirect('/kevin-admin/{0}/{1}'.format(app_name, table_name))
    return render(request, 'kevinadmin/table_obj_delete.html', locals())
