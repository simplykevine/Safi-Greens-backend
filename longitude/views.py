from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Location
from .serializers import LocationSerializer
from .utils import haversine_distance, reverse_geocode  

class CreateLocationView(APIView):
    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            lat = serializer.validated_data['latitude']
            lon = serializer.validated_data['longitude']
            address = reverse_geocode(lat, lon)
            serializer.save(address=address)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        List all locations (Mama Mboga and customers).
        """
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

class NearbyMamaMbogaView(APIView):
    def get(self, request):
        try:
            user_lat = float(request.query_params.get('latitude'))
            user_lon = float(request.query_params.get('longitude'))
            radius = float(request.query_params.get('radius', 5))  
        except (TypeError, ValueError):
            return Response({'error': 'Invalid or missing latitude/longitude.'}, status=400)

        mama_mbogas = Location.objects.filter(is_mama_mboga=True)
        nearby = []
        for mboga in mama_mbogas:
            distance = haversine_distance(user_lat, user_lon, mboga.latitude, mboga.longitude)
            if distance <= radius:
                mboga_data = LocationSerializer(mboga).data
                mboga_data['distance_miles'] = round(distance, 2)
                nearby.append(mboga_data)

        return Response(nearby)