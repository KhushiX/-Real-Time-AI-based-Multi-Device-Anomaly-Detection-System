from django.contrib import admin

# Register your models here.
from .models import SensorReading

@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_id', 'timestamp', 'battery', 'acc_x', 'acc_y', 'acc_z')
    list_filter = ('device_id',)
    ordering = ('-timestamp', '-id')   # newest first
    date_hierarchy = 'timestamp'
