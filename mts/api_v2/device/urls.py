from django.urls import re_path

from mts.api_v2.device.views import DeviceAdd, DeviceAllocate, DeviceAddExtend, DeviceInputData

urlpatterns = {
    re_path('add/(?P<pk>[0-9]+)?(/)?$', DeviceAdd.as_view()),
    re_path('allocate/(?P<pk>[0-9]+)?(/)?$', DeviceAllocate.as_view()),
    re_path('inputdata/(?P<pk>[0-9]+)?(/)?$', DeviceInputData.as_view()),
    re_path('extend/$', DeviceAddExtend.as_view()),
}