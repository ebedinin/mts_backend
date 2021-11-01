from rest_framework import serializers

from mts.models import Report, ReportDeviceProfileDetail


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('id', 'name', 'type', 'device_profile')


class ReportDeviceProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportDeviceProfileDetail
        fields = ('id', 'report', 'device_profile_field', 'value')
