from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.permissions import IsVendor, IsAdminUserType, IsVendorOrAdmin
from .models import Product, VendorProduct
from .serializers import ProductSerializer, VendorProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        # Anyone can list or retrieve
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        # Only vendors and admins can create, update, or delete
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsVendorOrAdmin()]
        # Default fallback
        return [IsAuthenticated()]

class VendorProductViewSet(viewsets.ModelViewSet):
    queryset = VendorProduct.objects.all()
    serializer_class = VendorProductSerializer

    def get_permissions(self):
        # Anyone can view vendor products
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        # Only vendors and admins can create, update, or delete
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsVendorOrAdmin()]
        return [IsAuthenticated()]