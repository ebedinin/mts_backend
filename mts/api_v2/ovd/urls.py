from django.urls import re_path

from mts.api_v2.ovd.views import OvdView, OvdExtend

urlpatterns = {
    re_path('item/(?P<pk>[0-9]+)?(/)?$', OvdView.as_view()),
    re_path('extend/(?P<pk>[0-9]+)?(/)?$', OvdExtend.as_view()),
}