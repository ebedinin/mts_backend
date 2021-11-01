from datetime import date, datetime
from django.db.models import Q
from pymysql import Date
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import logging
from certification_pc.models import PC, Object, Address, LogPcEdit, LogConnect, Nas, VipNet, VipnetType
from certification_pc.serializers import PCSerializer, ObjectSerializer, PCAdminSerializer, AddressSerializer, \
    LogPcSerializer, PCUpdateSerializer, LogConnectionSerializer, VipNetSerializer, LogIncludeVipnetPcSerializer
from certification_pc.serizlizers.vipnet import SvipNet, SvipnetType, SvipNetAdd
from mts.api_v2.common.common import ApiPageSearchFilter, TReturnAdd, OK, ERROR, TReturn, NOT_FOUND


class AddressView(ApiPageSearchFilter):
    model = Address
    serializer_class = AddressSerializer
    filter_fields = []  # ['department', 'ovd']
    search_fields = []
    permission_classes = (AllowAny,)
    filters = Q(isActive=True)
    default_page_size = 100
    def get(self, request, pk=None,format=None):
        print("GET")
        if pk:
            return Response(self.getInstance(request,pk), status=status.HTTP_200_OK)
        else:
            return Response(self.getList(request), status=status.HTTP_200_OK)

class PCView(ApiPageSearchFilter):
    model = PC
    serializer_class = PCSerializer
    filter_fields = ['status']  # ['department', 'ovd']
    search_fields = []
    permission_classes = (AllowAny,)
    filters = Q(isActive=True)
    def get(self, request, pk=None,format=None):
        print("GET")
        ovd = int(self.request.query_params.get('ovd', 0))
        if (ovd):
            self.filters &= Q(ovd = ovd)
        mac = self.request.query_params.get('mac', "")
        if (mac!=""):
            self.filters &= Q(mac_address = mac)
        st = self.request.query_params.get('status', "")
        if (st!=""):
            self.filters &= Q(status = st)
        inventory_number = self.request.query_params.get('inventory_number', "")
        if (inventory_number!=""):
            self.filters &= Q(inventory_number__contains=inventory_number)
        if pk:
            print("getInstance")
            return Response(self.getInstance(request,pk), status=status.HTTP_200_OK)
        else:
            print("getList")
            return Response(self.getList(request), status=status.HTTP_200_OK)
    def post(self, request, format=None):
        #ser = PCSerializer(data=request.data)
        #pc = ser.save()
        return Response(self.add(request),status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        print("DELETE")
        return Response(self.remove(request, pk),status=status.HTTP_200_OK)
    def put(self, request, pk, format=None):
        serializer_old = self.serializer_class
        #self.serializer_class = PCUpdateSerializer
        print("PUT")
        #s = self.serializer_class(data=request.data)
        #print(s.is_valid())
        #print(s.validated_data)
        try:
            obj = self.model.objects.get(id=pk)
            obj.status = PC.STATUS[2][0]
            obj.date_edit = date.today()
            print(obj.date_apply)
            serializer = PCUpdateSerializer(instance=obj, data=request.data)
            print("1")
            if serializer.is_valid():
                print(serializer.validated_data)
                pc = serializer.save()
                print(datetime.today().strftime("%Y-%m-%d"))
                print(pc.date_apply)
                return Response(TReturnAdd(data=serializer.data, code=OK).make())
            else:
                return Response(TReturn(code=ERROR,text=str(serializer.errors)).make())
        except self.model.DoesNotExist:
            return Response(TReturn(code=NOT_FOUND).make())
        except Exception as e:
            return Response(TReturn(code=ERROR,text=str(e)).make())


class PCAdminView(PCView):
    serializer_class = PCAdminSerializer

class ObjectView(ApiPageSearchFilter):
    model = Object
    serializer_class = ObjectSerializer
    filter_fields = []  # ['department', 'ovd']
    search_fields = []
    permission_classes = (AllowAny,)
    filters = Q(isActive=True)
    default_page_size = 100
    def get(self, request, pk=None,format=None):
        print("GET")
        ovd = int(self.request.query_params.get('ovd', 0))
        if (ovd):
            self.filters &= Q(ovd__id = ovd)
        if pk:
            return Response(self.getInstance(request,pk), status=status.HTTP_200_OK)
        else:
            return Response(self.getList(request), status=status.HTTP_200_OK)

    #def post(self, request, format=None):
    #    #ser = PCSerializer(data=request.data)
    #    #pc = ser.save()
    #    return Response(self.add(request),status=status.HTTP_200_OK)
#
    #def delete(self, request, pk, format=None):
    #    print("DELETE")
    #    return Response(self.remove(request, pk),status=status.HTTP_200_OK)
    #def put(self, request, pk, format=None):
    #    print("PUT")
    #    return Response(self.update(request, pk),status=status.HTTP_200_OK)

class LogView(ApiPageSearchFilter):
    serializer_class = LogPcSerializer
    model = LogPcEdit
    filter_fields = []  # ['department', 'ovd']
    search_fields = []
    permission_classes = (AllowAny,)
    filters = Q(isActive=True)
    def post(self, request, format=None):
        #ser = PCSerializer(data=request.data)
        #pc = ser.save()
        #self.add(request)
        return Response(self.add(request), status=status.HTTP_200_OK)



class LogConnectView(ApiPageSearchFilter):
    serializer_class = LogConnectionSerializer
    model = LogConnect
    filter_fields = []  # ['department', 'ovd']
    search_fields = []
    permission_classes = (AllowAny,)
    filters = Q()#Q(isActive=True)
    print(1)
    def post(self, request, format=None):
        try:
            print(request.data)
            print(2)
            serializer = self.serializer_class(data=request.data)
            print(3)
            if serializer.is_valid():
                print(4)
                mac_address = serializer.data['mac_address'].replace("-",":")
                pc = PC.objects.get(mac_address=mac_address)
                if (pc):
                    nas = Nas.objects.get(ip=serializer.data['nas_ip_address'])
                    if (nas):
                        log = LogConnect(nas=nas, pc=pc, mac_address=mac_address)
                        log.save()
                    return Response(TReturn(code=OK).make(), status=status.HTTP_200_OK)
                else:
                    return Response(TReturn(code=NOT_FOUND).make(), status=status.HTTP_200_OK)
            print(serializer.errors)
        except Exception as k:
            print(k)
            return Response(TReturn(code=NOT_FOUND, text="No PC or NAS found").make(), status=status.HTTP_200_OK)

class VipNetView(ApiPageSearchFilter):
    model = VipNet
    serializer_class = VipNetSerializer
    filter_fields = []  # ['department', 'ovd']
    search_fields = []
    permission_classes = (AllowAny,)
    filters = Q(isActive=True)
    default_page_size = 100

    def get(self, request, pk=None, format=None):
        print("GET")
        identifier = self.request.query_params.get('identifier', "")
        if (identifier != ""):
            self.filters &= Q(identifier=identifier)
        pc_id = self.request.query_params.get('pc_id', "")
        if (pc_id != ""):
            self.filters &= Q(pc=pc_id)
        if pk:
            return Response(self.getInstance(request, pk), status=status.HTTP_200_OK)
        else:
            return Response(self.getList(request), status=status.HTTP_200_OK)

class VipNetTypeView(ApiPageSearchFilter):
    model = VipnetType
    serializer_class = SvipnetType
    filter_fields = []  # ['department', 'ovd']
    search_fields = []
    permission_classes = (AllowAny,)
    filters = Q(isActive=True)
    default_page_size = 100

    def get(self, request, pk=None, format=None):
        print("GET")
        if pk:
            return Response(self.getInstance(request, pk), status=status.HTTP_200_OK)
        else:
            return Response(self.getList(request), status=status.HTTP_200_OK)

class VipNetWebView(ApiPageSearchFilter):
    model = VipNet
    serializer_class = SvipNet
    filter_fields = []  # ['department', 'ovd']
    search_fields = []
    permission_classes = (AllowAny,)
    filters = Q(isActive=True)
    default_page_size = 100

    def get(self, request, pk=None, format=None):
        print("GET")
        identifier = self.request.query_params.get('identifier', "")
        if (identifier != ""):
            self.filters &= Q(identifier=identifier)
        search = self.request.query_params.get('search', "")
        if(search != ""):
            self.filters &= Q(identifier__icontains=search) | \
                        Q(name__icontains=search) | \
                        Q(ip_real__icontains=search) | \
                        Q(ip_virtual__icontains=search) | \
                        Q(pc__name__icontains=search) | \
                        Q(note__icontains=search) | \
                        Q(description__icontains=search)
        pc_id = self.request.query_params.get('pc_id', "")
        if (pc_id != ""):
            self.filters &= Q(pc=pc_id)
        print(self.filters)
        if pk:
            return Response(self.getInstance(request, pk), status=status.HTTP_200_OK)
        else:
            return Response(self.getList(request), status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        try:
            obj = self.model.objects.get(id=pk)
            serializer = VipNetSerializer(instance=obj, data=request.data)
            if serializer.is_valid():
                vipnet = serializer.save()
                #print(datetime.today().strftime("%Y-%m-%d"))
                #print(pc.date_apply)
                obj = self.model.objects.get(id=pk)
                serializer = self.serializer_class(instance=obj)
                return Response(TReturnAdd(data=serializer.data, code=OK).make())
            else:
                return Response(TReturn(code=ERROR, text=str(serializer.errors)).make())
        except self.model.DoesNotExist:
            return Response(TReturn(code=NOT_FOUND).make())
        except Exception as e:
            return Response(TReturn(code=ERROR, text=str(e)).make())

    def post(self, request, format=None):
        serializer_old = self.serializer_class
        self.serializer_class = SvipNetAdd
        data = self.add(request)
        self.serializer_class = serializer_old
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        return Response(self.remove(request, pk))
