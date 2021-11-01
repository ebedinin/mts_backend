from rest_framework import serializers

# Устройство
from rest_framework.fields import CharField, BooleanField, DateTimeField, IPAddressField, IntegerField

from certification_pc.models import Object, Address, PC, LogPcEdit, VipNet
from mts.api_v2.department.serializers import DepartmentSerializer
from mts.api_v2.device.serializers import FieldSerializer
from mts.api_v2.ovd.serializers import OvdSerializer
from mts.models import Device, Ovd, Department, Nomenclature


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'address')

class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object
        fields = ('id', 'name', 'ovd', 'department', 'address')
        depth = 0


class PCSerializer(serializers.ModelSerializer):
    class Meta:
        model = PC
        fields = ('id',
                  'name',
                  'serial_number',
                  'inventory_number',
                  'isUnknownInventoryNumber',
                  'price_start_up',
                  'user',
                  'bailee',
                  'note',
                  'object',
                  'ovd',
                  'department',
                  'inventory_number_other',
                  'room',
                  'mac_address',
                  'ip_address',
                  'host_name',
                  'hard_serial_number',
                  'hard_name',
                  'os',
                  'secret_net_studio_version',
                  'crypto_pro_version',
                  'vipnet_client_version',
                  'kaspersky_version',
                  'status',
                  'date_apply',
                  'date_edit')
        read_only_fields = ['id',
                            'name',
                            'serial_number',
                            'inventory_number',
                            'price_start_up',
                            'bailee',
                            'note',
                            'ovd',
                            'status',
                            'date_apply',
                            'date_edit']


class PсFull(serializers.ModelSerializer):
    class Meta:
        model = PC
        fields = ('id',
                  'name',
                  'serial_number',
                  'inventory_number',
                  'isUnknownInventoryNumber',
                  'price_start_up',
                  'user',
                  'bailee',
                  'note',
                  'object',
                  'ovd',
                  'department',
                  'inventory_number_other',
                  'room',
                  'mac_address',
                  'ip_address',
                  'host_name',
                  'hard_serial_number',
                  'hard_name',
                  'os',
                  'secret_net_studio_version',
                  'crypto_pro_version',
                  'vipnet_client_version',
                  'kaspersky_version',
                  'status',
                  'date_apply',
                  'date_edit')
        read_only_fields = ['id',
                            'name',
                            'serial_number',
                            'inventory_number',
                            'price_start_up',
                            'bailee',
                            'note',
                            'ovd',
                            'status',
                            'date_apply',
                            'date_edit']



class VipNetSerializer(serializers.ModelSerializer):
    #pc = PCSerializer()
    class Meta:
        model = VipNet
        fields = ('id', 'identifier', 'name', 'date_create', 'date_remove', 'ip_real', 'ip_virtual', 'pc',
                  'vipnet_type', 'last_date_locked', 'isLocked')


class LogPcSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogPcEdit
        fields = ('mac_address',
                  'ip_address',
                  'host_name',
                  'hard_name',
                  'os',
                  'secret_net_studio_version',
                  'crypto_pro_version',
                  'vipnet_client_version',
                  'kaspersky_version',
                  'vipnet_identifier'
                  )

class LogIncludeVipnetPcSerializer(LogPcSerializer):
    class Meta:
        model = LogPcEdit
        fields = ('vipnet_identifier')


class PCUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PC
        fields = ('id',
                  'user',
                  'object',
                  'room',
                  'mac_address',
                  'ip_address',
                  'host_name',
                  'hard_name',
                  'os',
                  'secret_net_studio_version',
                  'crypto_pro_version',
                  'vipnet_client_version',
                  'department',
                  'kaspersky_version'
                  )
        read_only_fields = ['id']


class PCAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = PC
        fields = ('id',
                  'name',
                  'serial_number',
                  'inventory_number',
                  'isUnknownInventoryNumber',
                  'price_start_up',
                  'user',
                  'bailee',
                  'note',
                  'object',
                  'inventory_number_other',
                  'room',
                  'mac_address',
                  'ip_address',
                  'host_name',
                  'hard_serial_number',
                  'hard_name',
                  'os',
                  'secret_net_studio_version',
                  'crypto_pro_version',
                  'vipnet_client_version',
                  'kaspersky_version',
                  'status',
                  'date_apply',
                  'date_edit',
                  'department')
        read_only_fields = ['id',
                            'name',
                            'serial_number',
                            'inventory_number',
                            'isUnknownInventoryNumber',
                            'price_start_up',
                            'user',
                            'bailee',
                            'note',
                            'object',
                            'inventory_number_other',
                            'room',
                            'mac_address',
                            'ip_address',
                            'host_name',
                            'hard_serial_number',
                            'hard_name',
                            'os',
                            'secret_net_studio_version',
                            'crypto_pro_version',
                            'vipnet_client_version',
                            'kaspersky_version',
                            'date_apply',
                            'department',
                            'date_edit']

class LogConnectionSerializer(serializers.Serializer):
    mac_address = serializers.CharField(max_length=17)
    nas_ip_address = serializers.IPAddressField()