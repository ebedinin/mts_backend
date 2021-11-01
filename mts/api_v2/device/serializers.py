from rest_framework import serializers

# Устройство
from mts.models import Device, Department, Nomenclature, DeviceDetail


class DeviceAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'name', 'serial_number', 'price_start_up', 'provisioner', 'delivery_plan', 'invoice')

class DeviceAddExtendSerializer(serializers.ModelSerializer):

    inventory_number = serializers.CharField(max_length=15)
    mac_address = serializers.CharField(max_length=12)
    ip_address = serializers.CharField()


class DeviceAllocateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = (
            'id', 'name', 'serial_number', 'price_start_up', 'provisioner', 'delivery_plan', 'invoice', 'ovd',
            'department',
            'nomenclature')

    def validate(self, data):
    #    department = None
        ovd = data['ovd']
        if ovd:
            try:
                department = Department.objects.get(id=data['department'].id, ovd=ovd)
            except:
                print("department")
                raise serializers.ValidationError("Not found Department")
            try:
                Nomenclature.objects.get(id=data['nomenclature'].id, department=department)
            except:
                print("nomenclature")
                raise serializers.ValidationError
        return data

class FieldSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=False)
    value = serializers.CharField()
    def create(self, validated_data):
        print("FieldSerializer:create")
        print(validated_data)
        return Field(**validated_data)

class DeviceProfileDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=False)
    fields = FieldSerializer(many=True)
    def create(self, validated_data):
        print("DeviceProfileDetailSerializer:create")
        print(validated_data)
        return DeviceProfileDetailItem(**validated_data)

class DeviceDetailSerializer(serializers.Serializer):
    ovd = serializers.IntegerField(allow_null=False)
    department = serializers.IntegerField(allow_null=False)
    inventory_number = serializers.CharField(max_length=50)
    detail = DeviceProfileDetailSerializer(many=True)

    def create(self, validated_data):
        print("create")
        print(validated_data)
        return DeviceDetailItem(**validated_data)

class DeviceInputDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'name', 'serial_number', 'inventory_number', 'price_start_up', 'ovd')

class Field:
    def __init__(self, id, value):
        self.id = id
        self.value = value
class DeviceProfileDetailItem:
    def __init__(self, id, fields):
        self.id = id
        self.field = fields

class DeviceDetailItem:
    def __init__(self, ovd, department, inventory_number, detail):
        self.ovd = ovd
        self.department = department
        self.inventory_number = inventory_number
        self.detail = detail