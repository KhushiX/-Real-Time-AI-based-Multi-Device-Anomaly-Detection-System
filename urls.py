from django.urls import path
from .views import SensorReadingCreate, latest_rows
from .views import fetch_unified_activity


urlpatterns = [
    # POST from Android (unchanged)
    path("readings/", SensorReadingCreate.as_view(), name="sensor-reading-create"),

    # NEW GET: raw latest rows
    path("readings/latest_rows/", latest_rows, name="readings-latest-rows"),
]
from .views import create_device_event, create_unified_activity

urlpatterns = [
    # existing urls
    path('device-event/', create_device_event),
    path('unified-activity/', create_unified_activity),
    path('unified-activity-data/', fetch_unified_activity),
]
