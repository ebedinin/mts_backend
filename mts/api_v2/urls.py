from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

urlpatterns = {
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),
    path('device/', include('mts.api_v2.device.urls')),
    path('ovd/', include('mts.api_v2.ovd.urls')),
    path('department/', include('mts.api_v2.department.urls')),
    path('deviceprofile/', include('mts.api_v2.deviceProfile.urls')),
    path('report/', include('mts.api_v2.report.urls')),
}

urlDeviceAdd = {

}

urlpatterns = format_suffix_patterns(urlpatterns)
