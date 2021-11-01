from rest_framework import serializers

from certification_pc.models import VipNet, PC, Object, Address, VipnetType
from mts.models import Department, Ovd


class Saddress(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'address')

class SvipnetType(serializers.ModelSerializer):
    class Meta:
        model = VipnetType
        fields = ('id', 'name')

class Sobject(serializers.ModelSerializer):
    address = Saddress()
    class Meta:
        model = Object
        fields = ('id', 'name', 'address')
        depth = 0
class Sdepartment(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name_abbreviation')
class Sovd(serializers.ModelSerializer):
    class Meta:
        model = Ovd
        fields = ('id', 'name_abbreviation')

class Spc(serializers.ModelSerializer):
    object = Sobject()
    ovd = Sovd()
    department = Sdepartment()
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



class SvipNet(serializers.ModelSerializer):
    pc = Spc()
    vipnet_type = SvipnetType()
    class Meta:
        model = VipNet
        fields = ('id', 'identifier', 'name', 'date_create', 'date_remove', 'ip_real', 'ip_virtual', 'pc',
                  'vipnet_type', 'last_date_locked', 'isLocked')
class SvipNetAdd(serializers.ModelSerializer):
    class Meta:
        model = VipNet
        fields = ('id', 'identifier', 'name', 'date_create', 'date_remove', 'ip_real', 'ip_virtual', 'pc',
                  'vipnet_type', 'last_date_locked', 'isLocked')