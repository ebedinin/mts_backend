from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from mts.api_v2.common.common import ApiPageSearchFilterDeviceAllocate, TReturnAdd, OK, ApiPageSearchFilter, ERROR, \
    REPEAT
from mts.api_v2.device.serializers import DeviceDetailSerializer, DeviceProfileDetailSerializer, FieldSerializer, \
    DeviceAddSerializer, DeviceInputDataSerializer
from rest_framework.renderers import JSONRenderer

from mts.models import Device, DeviceStatus


class ApiPageSearchFilterDeviceAdd(ApiPageSearchFilter):
    model = Device
    serializer_class = DeviceAddSerializer
    filter_fields = []  # ['department', 'ovd']
    search_fields = ['name', 'serial_number', 'inventory_number']
    status = None
    try:
        status = DeviceStatus.objects.get(name=DeviceStatus.STATUS_DEVICE[9][0])
    except:
        pass
    filters = Q(isActive=True) & Q(status__in=[status])
    def add(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                device = serializer.save()
                status = DeviceStatus.objects.get(name=DeviceStatus.STATUS_DEVICE[9][0])
                device.status.add(status)
                status = DeviceStatus.objects.get(name=DeviceStatus.STATUS_DEVICE[0][0])
                device.status.add(status)
            except:
                return TReturnAdd(code=ERROR).make()
            return TReturnAdd(data=serializer.data, code=OK).make()
        else:
            return TReturnAdd(code=ERROR).make()
class DeviceAdd(ApiPageSearchFilterDeviceAdd):
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

class DeviceAllocate(ApiPageSearchFilterDeviceAllocate):
    def get(self, request, pk=None,format=None):
        print("GET")
        if pk:
            return Response(self.getInstance(request,pk), status=status.HTTP_200_OK)
        else:
            return Response(self.getList(request), status=status.HTTP_200_OK)
    def delete(self, request, pk, format=None):
        print("DELETE")
        return Response(self.remove(request, pk),status=status.HTTP_200_OK)
    def put(self, request, pk, format=None):
        print("PUT")
        return Response(self.update(request, pk),status=status.HTTP_200_OK)
    def post(self, request, format=None):
        print("POST")
        return Response(self.add(request),status=status.HTTP_200_OK)

class DeviceAddExtend(APIView):
    #serializer_class = DeviceAddExtendSerializer
    permission_classes = (AllowAny,)
    #print("1")
    def post(self, request, format=None):
        print(request.data)
        serializer = DeviceDetailSerializer(data=request.data)
        tmp = serializer.save()
        print(tmp.inventory_number)
        #json = JSONRenderer().render(serializer)
        #print(serializer)
        #print(serializer.initial_data)
        #print(json)
        return Response(TReturnAdd(serializer.validated_data, code=OK).make(),status=status.HTTP_200_OK)

class DeviceInputData(ApiPageSearchFilter):
    model = Device
    serializer_class = DeviceInputDataSerializer
    filter_fields = []  # ['department', 'ovd']
    search_fields = ['name', 'serial_number', 'inventory_number']
    status = None
    try:
        status = DeviceStatus.objects.get(name=DeviceStatus.STATUS_DEVICE[8][0])
    except:
        pass
    filters = Q(isActive=True) & Q(status__in=[status])
    def add(self, request):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            device = Device(**serializer.validated_data)
            query = Q(inventory_number__contains = device.inventory_number) | Q(serial_number__contains = device.serial_number)
            query &= Q(ovd = device.ovd)
            device = Device.objects.filter(query)
            if (len(device) != 0):
                 return TReturnAdd(code=REPEAT).make()
            try:
                device = serializer.save()
                status = DeviceStatus.objects.get(name=DeviceStatus.STATUS_DEVICE[8][0])
                device.status.add(status)
                status = DeviceStatus.objects.get(name=DeviceStatus.STATUS_DEVICE[0][0])
                device.status.add(status)
            except:
                return TReturnAdd(code=ERROR).make()
            return TReturnAdd(data=serializer.data, code=OK).make()
        else:
            print(serializer.errors)
            return TReturnAdd(code=ERROR).make()

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