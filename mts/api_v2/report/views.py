from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from mts.api_v2.report.serializers import ReportSerializer, \
    ReportDeviceProfileDetailSerializer
from mts.api_v2.common.common import ApiPageSearchFilter, TReturn, ERROR, OK, TReturnInstance, NOT_FOUND, TReturnList
from mts.models import Report, ReportDeviceProfileDetail, Device


class ReportView(ApiPageSearchFilter):
    model = Report
    serializer_class = ReportSerializer
    filter_fields = []  # ['department', 'ovd']
    search_fields = []
    filters = Q(isActive=True)
    def get(self, request, pk=None,format=None):
        print("GET")
        if pk:
            return Response(self.getInstance(request,pk), status=status.HTTP_200_OK)
        else:
            return Response(self.getList(request), status=status.HTTP_200_OK)

    def post(self, request, format=None):
        print("POST")
        print(request.data)
        return Response(self.add(request),status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        print("DELETE")
        return Response(self.remove(request, pk),status=status.HTTP_200_OK)
    def put(self, request, pk, format=None):
        print("PUT")
        return Response(self.update(request, pk),status=status.HTTP_200_OK)

class ReportDeviceProfileDetailView(ApiPageSearchFilter):
    model = ReportDeviceProfileDetail
    serializer_class = ReportDeviceProfileDetailSerializer
    filter_fields = []  # ['department', 'ovd']
    search_fields = []
    filters = Q(isActive=True)
    def get(self, request, pk=None,format=None):
        print("GET")
        if pk:
            return Response(self.getInstance(request,pk), status=status.HTTP_200_OK)
        else:
            report_device_profile = int(self.request.query_params.get('report_device_profile', 0))
            if report_device_profile:
                self.filters &= Q(report_device_profile=report_device_profile)
            return Response(self.getList(request), status=status.HTTP_200_OK)

    def post(self, request, format=None):
        print("POST")
        return Response(self.add(request),status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        print("DELETE")
        return Response(self.remove(request, pk),status=status.HTTP_200_OK)
    def put(self, request, pk, format=None):
        print("PUT")
        return Response(self.update(request, pk),status=status.HTTP_200_OK)

class ReportMaker(APIView):
    model = Report
    def get(self,  request, pk=None, format=None):

        if pk:
            report = None
            try:
                print(pk)
                report = Report.objects.get(id=pk)
                if report.type == Report.TYPE[0][0]:
                    reportDeviceProfileDetail = ReportDeviceProfileDetail.objects.filter(report=report, isActive=True)
                    query = Q()
                    for item in reportDeviceProfileDetail:
                        query |= Q(devicedetail__id = item.device_profile_field_id) & Q(devicedetail__value__contains =item.value) & Q(devicedetail__isActive=True)
                    query &= Q(isActive=True)
                    print(Device.objects.filter(query).query)

                    return Response(TReturn(code=ERROR).make(),status=status.HTTP_200_OK)
            except self.model.DoesNotExist:
                return Response(TReturnInstance(code=NOT_FOUND).make())
            pass
        else:
            return Response(TReturn(code=ERROR).make(),status=status.HTTP_200_OK)
    def post(self, request, format=None):
        return Response(TReturn(code=ERROR).make(),status=status.HTTP_200_OK)
    def delete(self, request, pk, format=None):
        return Response(TReturn(code=ERROR).make(),status=status.HTTP_200_OK)
    def put(self, request, pk, format=None):
        return Response(TReturn(code=ERROR).make(),status=status.HTTP_200_OK)

    def reportDeviceProfile(self, report):
        profiles = report.device_profile
        query = Q()
        for profile in profiles:
            subQuery = Q(device_profile__in =[profile])

        return TReturnInstance(code=OK).make()