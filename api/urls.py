from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ProductViewSet,SubscriptionBoxViewSet, ScheduledItemViewSet, PaymentViewSet, OrderViewSet, UserViewSet, OrderItemViewSet,
    TestView,MakePayment, STKPushCallbackView, ApiRootView, OrderItemViewSet)
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
from .views import (
    ProductViewSet, VendorProductViewSet, SubscriptionBoxViewSet, ScheduledItemViewSet, 
    PaymentViewSet, OrderViewSet, OrderItemViewSet, UserViewSet, CartViewSet, CartItemViewSet
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'vendor-products', VendorProductViewSet, basename='vendorproduct')
router.register(r'subscriptions', SubscriptionBoxViewSet, basename='subscriptionbox')
router.register(r'scheduled-items', ScheduledItemViewSet, basename='scheduleditem')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'order-items', OrderItemViewSet, basename='order-item')
router.register(r'users', UserViewSet, basename='users')
router.register(r'payments', PaymentViewSet, basename='payments')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'cart-item', CartItemViewSet, basename='cart-item')


urlpatterns = [
    path('', include(router.urls)),
    path('test/', TestView.as_view(), name='test'),
    path('make-payment/', MakePayment.as_view(), name='make-payment'),
    path('stkpush-callback/', STKPushCallbackView.as_view(), name='stkpush-callback'),
    path('', ApiRootView.as_view(), name='api-root'),
    path('initiate_payment/<int:amount>/<str:phone>/', MakePayment.as_view(), name='initiate_payment')
]










