from django.conf.urls import url
from . import views as vs

urlpatterns = [
    url(r'^$', vs.app_index, name='admin_index'),
    url(r'^(\w+)/$', vs.app_single, name='app_single'),
    url(r'^(\w+)/(\w+)/$', vs.table_obj_list, name="table_obj_list"),
    url(r'^(\w+)/(\w+)/add/$', vs.table_obj_add, name="table_obj_add"),
    url(r'^(\w+)/(\w+)/(\d+)/change/$', vs.table_obj_change, name="table_obj_change"),
    url(r'^(\w+)/(\w+)/(\d+)/delete/$', vs.table_obj_delete, name="table_obj_delete"),
]
