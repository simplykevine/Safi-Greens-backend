from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsCustomer
from .models import SubscriptionBox, ScheduledItem
from .serializers import SubscriptionBoxSerializer, ScheduledItemSerializer

class SubscriptionBoxViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionBox.objects.all()
    serializer_class = SubscriptionBoxSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

class ScheduledItemViewSet(viewsets.ModelViewSet):
    queryset = ScheduledItem.objects.all()
    serializer_class = ScheduledItemSerializer
    permission_classes = [IsAuthenticated, IsCustomer]