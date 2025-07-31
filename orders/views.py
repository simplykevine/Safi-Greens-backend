from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsCustomer, IsVendor, IsAdminUserType
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        # Anyone logged in can view orders (will filter in queryset)
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        # Only customers can create orders (place orders)
        elif self.action == 'create':
            return [IsAuthenticated(), IsCustomer()]
        # Only vendors/admins can update status (approve etc)
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsVendor() | IsAdminUserType()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        # Admins see all
        if getattr(user, "user_type", None) == "admin":
            return Order.objects.all()
        # Customers see their own orders
        elif getattr(user, "user_type", None) == "customer":
            return Order.objects.filter(buyer=user)
        # Vendors see orders for their products (assume you have a relation)
        elif getattr(user, "user_type", None) == "vendor":
            return Order.objects.filter(items__product__vendor=user).distinct()
        return Order.objects.none()

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]