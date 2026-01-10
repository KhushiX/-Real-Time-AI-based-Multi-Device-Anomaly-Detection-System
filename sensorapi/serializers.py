from rest_framework import serializers
from .models import SensorReading

class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = '__all__'
from .models import DeviceEvent

class DeviceEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceEvent
        fields = '__all__'

from .models import UnifiedDeviceActivity
class UnifiedDeviceActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UnifiedDeviceActivity
        fields = '__all__'

