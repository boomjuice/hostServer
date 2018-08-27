from django.template import Library
from django.utils.safestring import mark_safe
import datetime
import time

register = Library()


@register.simple_tag()
def build_filter_ele(filter_condition, admin_class):
    # filter_condition in list_filter = ['source', 'consultant', 'status', 'date']
    obj_column = admin_class.model._meta.get_field(filter_condition)
    filter_ele = "<div class='col-md-2'>%s:<select  class='form-control' name='%s'>" % (
        filter_condition, filter_condition)
    try:
        for choice in obj_column.get_choices():
            selected = ""
            if filter_condition in admin_class.filter_conditions:
                if str(choice[0]) == admin_class.filter_conditions.get(filter_condition):  # 当前值被选中了
                    selected = 'selected'

            option = "<option value ='%s' %s>%s</option>" % (choice[0], selected, choice[1])
            filter_ele += option
    except AttributeError as e:
        print(e)
        # date 特殊处理
        if obj_column.get_internal_type() in ('DateField', 'DateTimeField'):
            time_obj = datetime.datetime.now()
            time_list = [
                ('', '---------'),
                (time_obj, 'Today'),
                (time_obj - datetime.timedelta(7), '七天内'),
                (time_obj.replace(day=1), '本月内'),
                (time_obj - datetime.timedelta(90), '三个月内'),
                (time_obj.replace(month=1, day=1), '今年所有'),
            ]
            for i in time_list:
                selected = ""
                time_to_str = '' if not i[0] else i[0].strftime('%Y-%m-%d')
                if "%s__gte" % filter_condition in admin_class.filter_conditions:
                    if time_to_str == admin_class.filter_conditions.get("date__gte"): \
                            selected = 'selected'
                option = "<option value ='%s' %s>%s</option>" % (i[0], selected, i[1])
                filter_ele += option
    filter_ele += "</select></div>"
    return mark_safe(filter_ele)


@register.simple_tag()
def get_order_index(order_conditions):
    return list(order_conditions.values())[0] if order_conditions else ""


@register.simple_tag()
def build_data_from_th(obj, admin_class):
    ele = ""
    if admin_class.list_display:
        for index, list_name in enumerate(admin_class.list_display):
            obj_column = admin_class.model._meta.get_field(list_name)
            if obj_column.choices:
                column_data = getattr(obj, "get_%s_display" % list_name)()
            else:
                column_data = getattr(obj, list_name)
            td_ele = "<td>%s</td>" % column_data
            if index == 0:
                td_ele = "<td><a href='%s/change'>%s</a></td>" % (obj.id, column_data)
            ele += td_ele

    else:
        td_ele = "<td><a href='%s/change'>%s</a></td>" % (obj.id, obj)
        ele += td_ele
    return mark_safe(ele)


@register.simple_tag()
def get_model_name_upper(admin_class):
    return admin_class.model._meta.model_name.capitalize()


@register.simple_tag()
def get_app_name_lower(admin_class):
    return admin_class.model._meta.app_label


@register.simple_tag()
def get_model_name_lower(admin_class):
    return admin_class.model._meta.model_name


@register.simple_tag()
def get_model_verbose_name(admin_class):
    return admin_class.model._meta.verbose_name


@register.simple_tag()
def order_href_build(list_name, forloop, order_conditions):
    if list_name in order_conditions:
        previous_order_index = order_conditions[list_name]
        if previous_order_index.startswith('-'):
            next_order_index = previous_order_index.strip('-')
        else:
            next_order_index = '-%s' % (previous_order_index)
        return next_order_index
    else:
        return forloop


@register.simple_tag()
def filter_conditions_build(admin_class):
    if admin_class.filter_conditions:
        ele = ''
        for k, v in admin_class.filter_conditions.items():
            ele += "&%s=%s" % (k, v)
        return mark_safe(ele)
    else:
        return ''


@register.simple_tag()
def get_order_icon(list_name, order_conditions):
    if list_name in order_conditions:
        direction = ''
        previous_order_index = order_conditions[list_name]
        if previous_order_index.startswith('-'):
            direction = 'up'
        else:
            direction = 'down'
        ele = '<span class="glyphicon glyphicon-chevron-%s"></span>' % (direction)
        return mark_safe(ele)
    return ''


@register.simple_tag()
def get_obj_field_val(form_obj, field):
    """返回可读model的值在前端展示"""
    # form_obj.instance 拿到表对象 CustomerInfo
    return getattr(form_obj.instance, field)


@register.simple_tag()
def get_multiple_choices(admin_class, field_name, form_obj):
    """返回多对多表关联的数据 将已选数据移动到右边"""
    field_obj = admin_class.model._meta.get_field(field_name)
    obj_list = set(field_obj.related_model.objects.all())
    if form_obj.instance.id:
        selected_data = set(getattr(form_obj.instance, field_name).all())
        return obj_list - selected_data
    else:
        return obj_list


@register.simple_tag()
def get_multiple_selected_choices(field_name, form_obj):
    """返回多选框中已选的多对多数据"""
    if form_obj.instance.id:
        selected_data = getattr(form_obj.instance, field_name).all()
        return selected_data
    else:
        return []


@register.simple_tag()
def get_related_fk_dispaly(obj):
    ele = '<ul>'
    for reversed_fk_obj in obj._meta.related_objects:
        related_table_name = reversed_fk_obj.name
        if related_table_name == obj._meta.model_name:
            continue
        if reversed_fk_obj.get_internal_type() == 'OneToOneField':
            related_lookup_key = related_table_name
            if hasattr(obj, related_lookup_key):
                related_objs = getattr(obj, related_lookup_key)
                ele += '<li>%s</li>' % related_table_name
                ele += '<ul><li><a href="/kevin-admin/%s/%s/%s/change/">%s</a>记录里与[%s]相关的数据将被删除</li></ul>' \
                       % (
                       related_objs._meta.app_label, related_objs._meta.model_name, related_objs.id, related_objs, obj)
        else:
            related_lookup_key = '%s_set' % related_table_name
            related_objs = getattr(obj, related_lookup_key).all()  # 反向查找所有
            ele += '<li>%s<ul>' % related_table_name
            if reversed_fk_obj.get_internal_type() == 'ManyToManyField':  # 如果反向关联MTM字段则会关联到所有的字段
                for i in related_objs:
                    ele += '<li><a href="/kevin-admin/%s/%s/%s/change/">%s</a>记录里与[%s]相关的数据将被删除</li>' \
                           % (i._meta.app_label, i._meta.model_name, i.id, i, obj)
            else:
                for i in related_objs:
                    ele += '<li><a href="/kevin-admin/%s/%s/%s/change/">%s</a></li>' % (
                        i._meta.app_label, i._meta.model_name, i.id, i)
                    ele += get_related_fk_dispaly(i)
            ele += '</ul></li>'
    ele += '</ul>'
    return ele
