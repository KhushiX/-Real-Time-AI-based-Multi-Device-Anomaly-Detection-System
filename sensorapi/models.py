from django.db import models

class SensorReading(models.Model):
    device_id = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    battery = models.FloatField(null=True, blank=True)

    acc_x = models.FloatField(null=True, blank=True)
    acc_y = models.FloatField(null=True, blank=True)
    acc_z = models.FloatField(null=True, blank=True)

    gyro_x = models.FloatField(null=True, blank=True)
    gyro_y = models.FloatField(null=True, blank=True)
    gyro_z = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device_id} - {self.timestamp}"

# temporary alias to keep older imports/migrations working
SensorData = SensorReading

class DeviceEvent(models.Model):
    device_type = models.CharField(max_length=20)  
    # phone / watch / laptop

    device_id = models.CharField(max_length=100)

    event_type = models.CharField(max_length=50)
    # heart_rate, steps, cpu_usage, bluetooth_status

    event_value = models.CharField(max_length=100)
    # 120, "connected", "85%"

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device_type} - {self.event_type}"

class UnifiedDeviceActivity(models.Model):
    device_id = models.CharField(max_length=100)
    device_type = models.CharField(max_length=20)

    accel_level = models.CharField(max_length=20, null=True, blank=True)
    bluetooth_state = models.CharField(max_length=10, null=True, blank=True)
    screen_state = models.CharField(max_length=10, null=True, blank=True)

    input_activity = models.BooleanField(null=True, blank=True)
    activity_duration_sec = models.IntegerField(null=True, blank=True)
    event_frequency = models.IntegerField(null=True, blank=True)

    file_transfer = models.BooleanField(null=True, blank=True)
    data_transfer_mb = models.FloatField(null=True, blank=True)

    heart_rate = models.IntegerField(null=True, blank=True)
    battery_level = models.IntegerField(null=True, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

