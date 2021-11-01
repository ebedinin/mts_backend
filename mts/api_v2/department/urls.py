from django.urls import re_path

from mts.api_v2.department.views import DepartmentView, DepartmentExtend
from mts.api_v2.ovd.views import OvdView, OvdExtend

urlpatterns = {
    re_path('item/(?P<pk>[0-9]+)?(/)?$', DepartmentView.as_view()),
    re_path('extend', DepartmentExtend.as_view()),
}