from rest_framework import serializers

# Устройство
from mts.models import DeviceProfile, DeviceProfileField, DeviceDetail


class DeviceProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceProfile
        fields = ('id', 'name')

class DeviceProfileFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceProfileField
        fields = ('id', 'name', 'device_profile')

class DeviceProfileFieldsExtend(serializers.ModelSerializer):
    class Meta:
        model = DeviceProfileField
        fields = ('id','name')

class DeviceProfileExtendSerializer(serializers.ModelSerializer):
    fields = DeviceProfileFieldsExtend(many=True, read_only=True)
    class Meta:
        model = DeviceProfile
        fields = ('id','name', 'fields')

class DeviceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceDetail
        fields = ('id', 'device_profile_field', 'device', 'value')
