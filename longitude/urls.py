from django.urls import path
from .views import CreateLocationView, NearbyMamaMbogaView

urlpatterns = [
    path('locations/', CreateLocationView.as_view(), name='create_location'),
    path('nearby-mama-mbogas/', NearbyMamaMbogaView.as_view(), name='nearby_mama_mbogas'),
]