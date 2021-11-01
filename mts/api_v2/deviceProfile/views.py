from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from mts.api_v2.common.common import ApiPageSearchFilter, TReturn, ERROR, TReturnList, OK
from mts.api_v2.deviceProfile.serializers import DeviceProfileSerializer, DeviceProfileFieldSerializer, \
    DeviceProfileExtendSerializer
from mts.models import DeviceProfile, DeviceProfileField


class DeviceProfileView(ApiPageSearchFilter):
    model = DeviceProfile
    serializer_class = DeviceProfileSerializer
    filter_fields = []  # ['department', 'ovd']
    search_fields = []
    filters = Q(isActive=True)

    def get(self, request, pk=None, format=None):
        print("DeviceProfile")
        if pk:
            return Response(self.getInstance(request, pk), status=status.HTTP_200_OK)
        else:
            return Response(self.getList(request), status=status.HTTP_200_OK)

    def post(self, request, format=None):
        print("POST")
        return Response(self.add(request), status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        print("DELETE")
        return Response(self.remove(request, pk), status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        print("PUT")
        return Response(self.update(request, pk), status=status.HTTP_200_OK)


class DeviceProfileFieldView(ApiPageSearchFilter):
    model = DeviceProfileField
    serializer_class = DeviceProfileFieldSerializer
    filter_fields = []  # ['department', 'ovd']
    search_fields = []
    filters = Q(isActive=True)

    def get(self, request, pk=None, format=None):
        print("DeviceProfileField")
        if pk:
            return Response(self.getInstance(request, pk), status=status.HTTP_200_OK)
        else:
            device_profile = self.request.query_params.getlist('device_profile', [])
            print(device_profile)
            if device_profile:
                self.filters &= Q(device_profile__in=device_profile)
            return Response(self.getList(request), status=status.HTTP_200_OK)

    def post(self, request, format=None):
        print("POST")
        return Response(self.add(request), status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        print("DELETE")
        return Response(self.remove(request, pk), status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        print("PUT")
        return Response(self.update(request, pk), status=status.HTTP_200_OK)


class DeviceProfileExtend(ApiPageSearchFilter):
    model = DeviceProfile
    serializer_class = DeviceProfileExtendSerializer
    filter_fields = []  # ['department', 'ovd']
    search_fields = []
    filters = Q(isActive=True)
    permission_classes = [AllowAny]
    default_page_size = 100
    default_page_number = 1

    def get(self, request, pk=None, format=None):

        if (self.model and self.serializer_class):
            # Формирования условий поиска
            query = self.filters
            instance = self.model.objects.filter(query)
            print(instance)
            serializer = self.serializer_class(instance=instance,many=True)
            print(serializer.data)
            rezult = TReturnList(serializer.data, 0, 0, 0)
            rezult.report.code = OK
            print(rezult)
            return Response(rezult.make(), status=status.HTTP_200_OK)
        else:
            return Response(TReturn(code=ERROR).make(), status=status.HTTP_200_OK)
    def post(self, request, format=None):
        return Response(TReturn(code=ERROR).make(), status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        return Response(TReturn(code=ERROR).make(), status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        return Response(TReturn(code=ERROR).make(), status=status.HTTP_200_OK)
