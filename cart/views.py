from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsCustomer
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated, IsCustomer]