# sensorapi/views.py
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import SensorReading
from .serializers import SensorReadingSerializer

# Existing POST view (unchanged)
class SensorReadingCreate(APIView):
    def post(self, request, *args, **kwargs):
        # DEBUG: print the raw incoming JSON payload to the server terminal
        print("DEBUG INCOMING PAYLOAD:", request.data)

        serializer = SensorReadingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# NEW: return latest raw DB rows (flat list)
@api_view(['GET'])
@permission_classes([AllowAny])
def latest_rows(request):
    """
    Return latest raw SensorReading rows as a flat list.
    Query params:
      - limit (int, default 50) : how many rows to return (most recent first)
      - device_id (optional) : filter by device_id
    Response:
      { "status": "ok", "count": N, "data": [ {<model fields>}, ... ] }
    """
    try:
        limit = int(request.query_params.get('limit', 50))
    except ValueError:
        limit = 50

    device = request.query_params.get('device_id')

    qs = SensorReading.objects.all().order_by('-created_at', '-timestamp')
    if device:
        qs = qs.filter(device_id=device)

    qs = qs[:limit]
    serializer = SensorReadingSerializer(qs, many=True)
    return Response({"status": "ok", "count": len(serializer.data), "data": serializer.data})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import DeviceEventSerializer
from .serializers import UnifiedDeviceActivitySerializer


@api_view(['POST'])
def create_device_event(request):
    serializer = DeviceEventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Device event stored"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_unified_activity(request):
    serializer = UnifiedDeviceActivitySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Unified activity stored"}, status=201)
    return Response(serializer.errors, status=400)

from .models import UnifiedDeviceActivity
from .serializers import UnifiedDeviceActivitySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def fetch_unified_activity(request):
    data = UnifiedDeviceActivity.objects.all().order_by('-timestamp')
    serializer = UnifiedDeviceActivitySerializer(data, many=True)
    return Response(serializer.data)
