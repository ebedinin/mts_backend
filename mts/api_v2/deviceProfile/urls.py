from django.urls import re_path

from mts.api_v2.deviceProfile.views import DeviceProfileView, DeviceProfileFieldView, DeviceProfileExtend

urlpatterns = {
    re_path('profile?/(?P<pk>[0-9]+)?(/)?$', DeviceProfileView.as_view()),
    re_path('field?/(?P<pk>[0-9]+)?(/)?$', DeviceProfileFieldView.as_view()),
    re_path('profileExtend/$', DeviceProfileExtend.as_view()),
    #re_path('value?/(?P<pk>[0-9]+)?(/)?$', DeviceProfileView.as_view()),
}