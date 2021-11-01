from django.urls import re_path

from mts.api_v2.report.views import ReportDeviceProfileDetailView, ReportView, ReportMaker

urlpatterns = {
    re_path('item/(?P<pk>[0-9]+)?(/)?$', ReportView.as_view()),
    re_path('deviceprofiledetail/(?P<pk>[0-9]+)?(/)?$', ReportDeviceProfileDetailView.as_view()),
    re_path('maker/(?P<pk>[0-9]+)?(/)?$', ReportMaker.as_view())
}