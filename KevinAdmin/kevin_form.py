from django.forms import ModelForm


def create_dynamic_model_form(admin_class, form_add=False):
    # form_add 为 True 时 为添加表单  False 为编辑表单
    class Meta:
        model = admin_class.model
        fields = "__all__"
        if not form_add:
            admin_class.form_add = False
            # 这是因为admin_class 只实例了一次 如果不加False赋值 那在添加之后再修改 可读字段还是能编辑
            exclude = admin_class.readonly_fields
        else:
            admin_class.form_add = True

    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({'class': 'form-control'})
            # if field_name in admin_class.readonly_fields:
            #     field_obj.widget.attrs.update({'disabled': 'true'})

        return ModelForm.__new__(cls)

    dynamic_form = type('DynamicModelForm', (ModelForm,), {'Meta': Meta, '__new__': __new__})
    return dynamic_form