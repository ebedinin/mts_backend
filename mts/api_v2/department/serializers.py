from rest_framework import serializers

# Устройство
from mts.models import Device, Ovd, Department, Nomenclature


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name_abbreviation', 'name_full', 'ovd')
