from rest_framework import serializers

# Устройство
from mts.models import Device, Ovd, Department, Nomenclature


class OvdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ovd
        fields = ('id', 'name_abbreviation', 'name_full')
