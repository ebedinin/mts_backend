from django.urls import re_path

from certification_pc.views import PCView, ObjectView, PCAdminView, AddressView, LogView, LogConnectView, VipNetView, \
    VipNetWebView, VipNetTypeView
from mts.api_v2.device.views import DeviceAdd, DeviceAllocate, DeviceAddExtend, DeviceInputData

urlpatterns = [
    re_path('pc/(?P<pk>[0-9]+)?(/)?$', PCView.as_view()),
    re_path('object/(?P<pk>[0-9]+)?(/)?$', ObjectView.as_view()),
    re_path('address/(?P<pk>[0-9]+)?(/)?$', AddressView.as_view()),
    re_path('vipnet/(?P<pk>[0-9]+)?(/)?$', VipNetView.as_view()),
    re_path('vipnettype/(?P<pk>[0-9]+)?(/)?$', VipNetTypeView.as_view()),
    re_path('vipnet/web/(?P<pk>[0-9]+)?(/)?$', VipNetWebView.as_view()),
    re_path('pc/log/?$', LogView.as_view()),
    re_path('pc/connect/$', LogConnectView.as_view()),
]