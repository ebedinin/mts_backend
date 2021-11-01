from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from mts.api_v2.common.common import ApiPageSearchFilter, TReturn, ERROR
from mts.api_v2.department.serializers import DepartmentSerializer
from mts.models import Ovd, Department


class DepartmentView(ApiPageSearchFilter):
    model = Department
    serializer_class = DepartmentSerializer
    filter_fields = []  # ['department', 'ovd']
    search_fields = []
    filters = Q(isActive=True)
    def get(self, request, pk=None,format=None):
        print("GET")
        if pk:
            return Response(self.getInstance(request,pk), status=status.HTTP_200_OK)
        else:
            ovd = int(self.request.query_params.get('ovd', 0))
            if ovd:
                self.filters &= Q(ovd=ovd)
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

class DepartmentExtend(DepartmentView):
    permission_classes = (AllowAny,)
    default_page_size = 100
    default_page_number = 1
    def get(self, request, pk=None,format=None):
        print("GET")
        ovd = int(self.request.query_params.get('ovd', 0))
        if ovd:
            self.filters = Q(ovd=ovd)
        return Response(self.getList(request), status=status.HTTP_200_OK)
    def post(self, request, format=None):
        return Response(TReturn(code=ERROR).make(),status=status.HTTP_200_OK)
    def delete(self, request, pk, format=None):
        return Response(TReturn(code=ERROR).make(), status=status.HTTP_200_OK)
    def put(self, request, pk, format=None):
        return Response(TReturn(code=ERROR).make(),status=status.HTTP_200_OK)
