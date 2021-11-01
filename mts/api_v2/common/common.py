# code
from django.core.paginator import Paginator
from django.db.models import Q, Count
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from mts.api_v2.device.serializers import DeviceAddSerializer, DeviceAllocateSerializer
from mts.models import DeviceStatus, Device

OK = 0
NOT_FOUND = 1
UNAUTHOROZED = 2
NOT_DELETE = 3
NOT_UPDATA = 4
ERROR = 5
REPEAT = 6

class TApiReport():
    def __init__(self):
        self._code = ERROR,
        self._text = ""

    def get_code(self):
        return self._code

    def set_code(self, value):
        self._code = value

    def del_code(self):
        self._code = ERROR

    code = property(get_code, set_code, del_code)
    def get_text(self):
        return self._text

    def set_text(self, value):
        self._text = value

    def del_text(self):
        self._text = ""

    text = property(get_text, set_text, del_text)

    def make(self):
        return {
            'code': self.code,
            'text': self.text,

        }

class TReturn():
    def __init__(self, code=ERROR, text=""):
        self.report = TApiReport()
        self.report.code = code
        self.report.text= text

    def make(self):
        return {
            'report': self.report.make()
        }

class TReturnList(TReturn):
    def __init__(self, data, page_number, page_size, count):
        super(TReturnList, self).__init__()
        self.data = data
        self.page_number = page_number
        self.page_size = page_size
        self.count = count

    def make(self):
        return {
            'report': self.report.make(),
            'page_number': self.page_number,
            'page_size': self.page_size,
            'count': self.count,
            'data': self.data
        }

class TReturnInstance(TReturn):
    def __init__(self, data=None, code=ERROR):
        super(TReturnInstance, self).__init__()
        self.data = data
        self.report.code = code

    def make(self):
        return {
            'report': self.report.make(),
            'data': self.data
        }

class TReturnAdd(TReturn):
    def __init__(self, data=None, code=ERROR, text=""):
        super(TReturnAdd, self).__init__()
        self.data = data
        self.report.code = code
        self.report.text = text

    def make(self):
        return {
            'report': self.report.make(),
            'data': self.data
        }

class ApiPageSearchFilter(APIView):
    model = None
    serializer_class = None
    search_fields = []
    filter_fields = []
    filters = None  # Дополнительные фильтры. Например статус устройства или isActive
    extend_filters = lambda self, p: p  # .annotate(total=Count('id')).filter(total=2)
    default_page_size = 10
    default_page_number = 1

    def getList(self, request):
        page_size = int(self.request.query_params.get('page_size', self.default_page_size))
        page_number = int(self.request.query_params.get('page_number', self.default_page_number))
        search = self.request.query_params.get('search')

        if (self.model and self.serializer_class):
            # Формирования условий поиска)
            query_search = Q()
            if search:
                for var in self.search_fields:
                    v = {var + "__contains": search}
                    query_search |= Q(**v)
            # Формирования условий фильтра
            query_filter = Q()
            for field_name in self.filter_fields:
                field_value = self.request.query_params.get(field_name, None)
                if (field_value):
                    v = {field_name: field_value}
                    query_filter &= Q(**v)

            # Формирования условий поиска
            query = query_search & query_filter
            if self.filters:
                query |= self.filters
            data = self.extend_filters(self.model.objects.filter(query))
            # Разбиение результата поиска по страницам
            paginator = Paginator(data, page_size)
            if (paginator.count // page_size < page_number):
                page_number = paginator.count // page_size + 1
            if (page_number < 1):
                page_number = 1
            # Сериализация нужной страници
            serializer = self.serializer_class(data=paginator.page(page_number), many=True,
                                               context={'request': request})
            serializer.is_valid()
            rezult = TReturnList(serializer.data, page_number, page_size, paginator.count)
            rezult.report.code = OK
            print(rezult)
            return rezult.make()
        else:
            print("ERROR1")
            rezult = TReturnList([], page_number, page_size, 0)
            rezult.report.code = ERROR
            return rezult.make()

    def getInstance(self, request, pk):
        try:
            obj = self.model.objects.get(id=pk, isActive=True)
            serializer = self.serializer_class(instance=obj)
            return TReturnInstance(data=serializer.data, code=OK).make()
        except self.model.DoesNotExist:
            return TReturnInstance(code=NOT_FOUND).make()

    def add(self, request):

        serializer = self.serializer_class(data=request.data)
        #return TReturnAdd(code=OK, text=str(request)).make()
        if serializer.is_valid():
            print("valid")
            serializer.save()
            return TReturnAdd(data=serializer.data, code=OK).make()
        else:
            print("invalid")
            return TReturnAdd(code=ERROR, text=str(serializer.errors)).make()

    def remove(self, request, pk):
        # Удаление
        try:
            obj = self.model.objects.get(id=pk)
            obj.isActive = False
            obj.save()
            return TReturn(code=OK).make()
        except self.model.DoesNotExist:
            return TReturn(code=NOT_FOUND).make()
        except:
            return TReturn(code=ERROR).make()

    def update(self, request, pk):
        try:
            obj = self.model.objects.get(id=pk)
            serializer = self.serializer_class(instance=obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return TReturnAdd(data=serializer.data, code=OK).make()
            else:
                return TReturn(code=ERROR).make()
        except self.model.DoesNotExist:
            return TReturn(code=NOT_FOUND).make()
        except:
            return TReturn(code=ERROR).make()



class ApiPageSearchFilterDeviceAllocate(ApiPageSearchFilter):
    model = Device
    serializer_class = DeviceAllocateSerializer
    filter_fields = ['department', 'ovd']
    search_fields = ['name', 'serial_number', 'inventory_number']
    DEVICE_ADD = DeviceStatus.objects.get(name=DeviceStatus.STATUS_DEVICE[9][0])
    UNALLOCATED = DeviceStatus.objects.get(name=DeviceStatus.STATUS_DEVICE[0][0])
    ALLOCATED = DeviceStatus.objects.get(name=DeviceStatus.STATUS_DEVICE[2][0])
    NOT_INVENTORY_NUMBER = DeviceStatus.objects.get(name=DeviceStatus.STATUS_DEVICE[1][0])
    filters = (Q(isActive=True) & Q(status__in=[DEVICE_ADD]) | Q(status__in=[UNALLOCATED]))
    extend_filters = lambda self, p: p.annotate(total=Count('id')).filter(total=2)

    def add(self, request):
        return TReturn(code=ERROR).make()

    def update(self, request, pk):
        try:
            obj = self.model.objects.get(id=pk)
            serializer = self.serializer_class(instance=obj, data=request.data)
            if serializer.is_valid():
                try:
                    device = serializer.save()
                    device.status.add(self.ALLOCATED)
                    device.status.add(self.NOT_INVENTORY_NUMBER)
                    device.status.remove(self.UNALLOCATED)
                    return TReturnAdd(data=serializer.data, code=OK).make()
                except:
                    return TReturnAdd(code=ERROR).make()
            else:
                return TReturn(code=ERROR).make()
        except self.model.DoesNotExist:
            return TReturn(code=NOT_FOUND).make()
        except:
            return TReturn(code=ERROR).make()

