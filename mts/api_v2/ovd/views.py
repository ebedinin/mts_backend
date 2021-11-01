from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from mts.api_v2.common.common import ApiPageSearchFilter, TReturn, ERROR
from mts.api_v2.ovd.serializers import OvdSerializer
from mts.models import Ovd


class OvdView(ApiPageSearchFilter):
    model = Ovd
    serializer_class = OvdSerializer
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
        return Response(self.add(request),status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        print("DELETE")
        return Response(self.remove(request, pk),status=status.HTTP_200_OK)
    def put(self, request, pk, format=None):
        print("PUT")
        return Response(self.update(request, pk),status=status.HTTP_200_OK)

class OvdExtend(OvdView):
    permission_classes = [AllowAny]
    default_page_size = 100
    default_page_number = 1
    def get(self, request, pk=None,format=None):
        print("GET")
        return Response(self.getList(request), status=status.HTTP_200_OK)
    def post(self, request, format=None):
        return Response(TReturn(code=ERROR).make(),status=status.HTTP_200_OK)
    def delete(self, request, pk, format=None):
        return Response(TReturn(code=ERROR).make(),status=status.HTTP_200_OK)
    def put(self, request, pk, format=None):
        return Response(TReturn(code=ERROR).make(),status=status.HTTP_200_OK)
