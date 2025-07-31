from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError, APIException
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.permissions import IsVendor, IsAdminUserType, IsVendorOrAdmin
from product.models import Product
from .serializers import ProductSerializer
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.conf import settings
from rest_framework import viewsets
from api.permissions import IsCustomer
from subscription.models import SubscriptionBox, ScheduledItem
from .serializers import SubscriptionBoxSerializer, ScheduledItemSerializer
import logging
import requests
import base64
from datetime import datetime
from product.models import Product, VendorProduct
from payment.models import Payment
from subscription.models import SubscriptionBox, ScheduledItem
from orders.models import Order, OrderItem
from cart.models import Cart, CartItem
from users.models import User
from .serializers import  ProductSerializer, VendorProductSerializer, PaymentSerializer, OrderSerializer,OrderItemSerializer, SubscriptionBoxSerializer, ScheduledItemSerializer, UserSerializer, CartSerializer, CartItemSerializer
from .access_token import generate_access_token
from .utils import timestamp_conversation
from .encode_base64 import generate_password
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
import base64
import requests
from datetime import datetime
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from payment.models import Payment, Order
logger = logging.getLogger(__name__)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from datetime import datetime
from base64 import b64encode
from decouple import config
import logging
from .serializers import PaymentSerializer  
from django.conf import settings
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsCustomer
from cart.models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from api.permissions import IsCustomer, IsVendor, IsAdminUserType
from orders.models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
class VendorProductViewSet(viewsets.ModelViewSet):
    queryset = VendorProduct.objects.all()
    serializer_class = VendorProductSerializer
    def perform_create(self, serializer):
        serializer.save()
    def perform_update(self, serializer):
        serializer.save()
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
class SubscriptionBoxViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionBox.objects.all()
    serializer_class = SubscriptionBoxSerializer
class ScheduledItemViewSet(viewsets.ModelViewSet):
    queryset = ScheduledItem.objects.all()
    serializer_class = ScheduledItemSerializer
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-order_date')
    serializer_class = OrderSerializer
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        qs = self.queryset
        if user_id:
            qs = qs.filter(buyer__user_id=user_id)
        return qs
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class=OrderItemSerializer
    def get_queryset(self):
        order_id = self.request.query_params.get('order')
        qs = self.queryset
        if order_id:
            qs = qs.filter(order_id=order_id)
        return qs

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['user_type']
    search_fields = ['name', 'phone_number', 'location', 'shop_name']
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        customer_name = self.request.data.get('customer_name') or self.request.query_params.get('customer_name')
        cart = None
        if customer_name:
            try:
                user = User.objects.get(name=customer_name, type='customer')
                cart, _ = Cart.objects.get_or_create(customer=user)
            except User.DoesNotExist:
                raise NotFound(f"Customer with name '{customer_name}' not found or not a customer.")
        context['cart'] = cart
        return context
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [AllowAny] 
    @action(detail=False, methods=['get'], url_path='by-customer')
    def get_cart_by_customer(self, request):
        customer_name = request.query_params.get('customer_name')
        if not customer_name:
            return Response(
                {"error": "customer_name query parameter is required"},
                status=400
            )
        try:
            user = User.objects.get(name=customer_name, type='customer')
        except User.DoesNotExist:
            raise NotFound(f"Customer with name '{customer_name}' not found or not a customer.")
        except User.MultipleObjectsReturned:
            raise ValidationError(
                f"Multiple customers found with name '{customer_name}'. Please use a unique identifier."
            )
        cart, created = Cart.objects.get_or_create(customer=user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=200)


class MPesaAPIException(Exception):
    pass

def generate_access_token():
    try:
        logger.info("Attempting to generate access token")
        response = requests.get(
            settings.ACCESS_TOKEN_URL,
            auth=(settings.CONSUMER_KEY, settings.CONSUMER_SECRET),
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.RequestException as e:
        logger.error(f"Failed to generate access token: {str(e)}")
        raise MPesaAPIException("Failed to generate access token.")

class TestView(APIView):
    def get(self, request, format=None):
        access_token = generate_access_token()
        formatted_time = timestamp_conversation()  
        decoded_password = generate_password(formatted_time) 
        return Response({
            "access_token": access_token,
            "decoded_password": decoded_password
        }, status=status.HTTP_200_OK)

class MakePayment(APIView):
    def post(self, request, *args, **kwargs):
        amount = request.data.get("amount")
        phone_number = request.data.get("phone_number")
        order_id = request.data.get("order_id")

        if not amount or not phone_number or not order_id:
            return Response(
                {"error": "Amount, phone_number, and order_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not (phone_number.startswith("254") and len(phone_number) == 12 and phone_number.isdigit()):
            return Response(
                {"error": "Invalid phone number format. Use 254 followed by 9 digits (e.g., 254712345678)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            order = Order.objects.get(order_id=order_id)
            if float(order.total_price) != float(amount):
                return Response(
                    {"error": "Amount does not match order total_price"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ObjectDoesNotExist:
            return Response(
                {"error": f"Order with ID {order_id} not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                payment_response_data = self.make_mpesa_payment_request(str(amount), str(phone_number), str(order_id))
                receiver_phone = config('RECEIVER_PHONE')
                self.notify_receiver(receiver_phone, amount, order_id, status="initiated")

                payment_data = {
                    "order": order.order_id,
                    "amount": amount,
                    "phone_number": phone_number,
                    "status": "pending",
                    "method": "M-Pesa",
                    "merchant_request_id": payment_response_data.get("MerchantRequestID"),
                    "checkout_request_id": payment_response_data.get("CheckoutRequestID"),
                }
                payment_serializer = PaymentSerializer(data=payment_data)
                if payment_serializer.is_valid():
                    payment_serializer.save()
                    logger.info(f"Initial payment record created: {payment_data}")
                else:
                    logger.error(f"Payment serializer errors: {payment_serializer.errors}")
                    return Response(
                        {"error": "Failed to save initial payment", "details": payment_serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(payment_response_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Payment request failed: %s", str(e), exc_info=True)
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def make_mpesa_payment_request(self, amount: str, phone: str, order_id: str) -> dict:
        try:

            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            payload = {
                "BusinessShortCode": BUSINESS_SHORT_CODE,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": TRANSACTION_TYPE,  
                "Amount": amount,
                "PartyA": phone,
                "PartyB": BUSINESS_SHORT_CODE,
                "PhoneNumber": phone,
                "CallBackURL": CALL_BACK_URL,
                "AccountReference": ACCOUNT_REFERENCE,
                "TransactionDesc": TRANSACTION_DESCRIPTION
            }

            logger.info("Sending M-Pesa STK Push request with payload: %s", payload)
            response = requests.post(STK_PUSH_URL, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            logger.error("HTTP error: %s, Response: %s", str(e), response.text if 'response' in locals() else "No response")
            raise MPesaAPIException(f"HTTP error: {str(e)}, Response: {response.text if 'response' in locals() else 'No response'}")
        except requests.RequestException as e:
            logger.exception("M-Pesa API connection failed")
            raise MPesaAPIException("Failed to connect to M-Pesa API. Reason: " + str(e))
        except Exception as e:
            logger.exception("Unexpected error during M-Pesa STK Push request")
            raise MPesaAPIException("Unexpected error: " + str(e))

    def generate_access_token(self, consumer_key: str, consumer_secret: str) -> str:
        try:
            credentials = f"{consumer_key}:{consumer_secret}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode('utf-8')
            headers = {
                'Authorization': f'Basic {encoded_credentials}',
                'Content-Type': 'application/json'
            }
            access_token_url = config('ACCESS_TOKEN_URL')
            response = requests.get(access_token_url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json().get('access_token')
        except requests.HTTPError as e:
            logger.error("Access Token Error: %s, Response: %s", str(e), response.text if 'response' in locals() else "No response")
            raise MPesaAPIException(f"Access Token Error: {str(e)}")
        except requests.RequestException as e:
            logger.exception("Failed to connect to M-Pesa OAuth API")
            raise MPesaAPIException("Failed to connect to M-Pesa OAuth API: " + str(e))
        except Exception as e:
            logger.exception("Unexpected error during access token generation")
            raise MPesaAPIException("Unexpected error: " + str(e))

    def notify_receiver(self, receiver_phone: str, amount: str, order_id: str, status: str):
        message = f"Payment of {amount} KSH for order {order_id} {status}."
        logger.info(f"Notification to receiver {receiver_phone}: {message}")
class STKPushCallbackView(APIView):
    def post(self, request, *args, **kwargs):
        logger.info(f"Raw request body: {request.body}")
        callback_data = request.data
        logger.info(f"Parsed request data: {callback_data}")

        try:
            if "Body" not in callback_data or "stkCallback" not in callback_data["Body"]:
                logger.error(f"Invalid callback data structure: {callback_data}")
                return Response(
                    {"error": "Invalid callback data structure"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            stk_callback = callback_data["Body"]["stkCallback"]
            result_code = stk_callback.get("ResultCode")
            result_desc = stk_callback.get("ResultDesc")
            merchant_request_id = stk_callback.get("MerchantRequestID")
            checkout_request_id = stk_callback.get("CheckoutRequestID")

            logger.info(f"Result Code: {result_code}, Result Description: {result_desc}")

            payment_data = {
                "merchant_request_id": merchant_request_id,
                "checkout_request_id": checkout_request_id,
                "result_code": result_code,
                "result_desc": result_desc,
            }


            if result_code == "0":  
                callback_metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])
                if not callback_metadata:
                    logger.error("CallbackMetadata is missing.")
                    return Response(
                        {"error": "CallbackMetadata is missing."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                for item in callback_metadata:
                    name = item.get("Name")
                    value = item.get("Value")
                    if name == "Amount":
                        payment_data["amount"] = value
                    elif name == "MpesaReceiptNumber":
                        payment_data["mpesa_receipt_number"] = value
                    elif name == "PhoneNumber":
                        payment_data["phone_number"] = value
                    elif name == "TransactionDate":
                        payment_data["transaction_date"] = parse_mpesa_date(value)

                payment_data["status"] = "success"
                logger.info(f"Payment successful: {payment_data}")
            else:
                payment_data["status"] = "failed"
                logger.warning(f"Payment failed: {result_desc} (ResultCode: {result_code})")

            try:
                with transaction.atomic():
                    payment = Payment.objects.get(checkout_request_id=checkout_request_id)
                    if payment_data.get("amount") and float(payment_data["amount"]) != float(payment.order.total_price):
                        logger.error(f"Amount mismatch: {payment_data['amount']} vs {payment.order.total_price}")
                        return Response(
                            {"error": "Amount in callback does not match order total_price"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    payment_serializer = PaymentSerializer(payment, data=payment_data, partial=True)
                    if payment_serializer.is_valid():
                        payment = payment_serializer.save()
                        logger.info(f"Payment record updated: {payment_data}")

                        if payment_data["status"] == "success":
                            order = payment.order
                            if order.status == "pending":
                                order.status = "paid"
                                order.save()
                                logger.info(f"Order {order.order_id} updated to paid status")
                                receiver_phone = config('RECEIVER_PHONE')
                                self.notify_receiver(receiver_phone, str(payment.amount), order.order_id, status="completed")
                        else:
                            logger.warning(f"Payment failed:{result_desc}(ResultCode:{result_code})")
                    else:
                        logger.error(f"Payment serializer errors: {payment_serializer.errors}")
                        return Response(
                            {"error": "Failed to update payment", "details": payment_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST
                        )
            except ObjectDoesNotExist:
                logger.error(f"No payment found for CheckoutRequestID: {checkout_request_id}")
                return Response(
                    {"error": f"No payment found for CheckoutRequestID: {checkout_request_id}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {"status": "success", "message": "Callback processed successfully"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.error(f"Unhandled exception during callback processing: {str(e)}", exc_info=True)
            return Response(
                {"error": "Failed to process callback", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

import africastalking

def notify_receiver(self, receiver_phone: str, amount: str, order_id: str, status: str):
    message = f"Payment of {amount} KSH for order {order_id} {status}."
    logger.info(f"Notification to receiver {receiver_phone}: {message}")
    africastalking.initialize(
            username=config('AFRICASTALKING_USERNAME'),
            api_key=config('AFRICASTALKING_API_KEY')
        )
    sms = africastalking.SMS
        
    try:
        response = sms.send(message, [receiver_phone])
        logger.info(f"SMS sent to {receiver_phone}: {response}")
    except Exception as e:
            logger.error(f"Failed to send SMS to {receiver_phone}: {str(e)}")
def parse_mpesa_date(date_str):
    try:
        return datetime.strptime(str(date_str), '%Y%m%d%H%M%S')
    except ValueError:
        logger.error(f"Invalid transaction date format: {date_str}")
        return None

class ApiRootView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            "message": "API root. Available endpoints: /payment/, /test/, /make-payment/, /stkpush-callback/"
        }, status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        # List (GET) and retrieve (GET detail): allow anyone
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        # Create (POST): Only vendors/admins
        elif self.action == 'create':
            return [IsAuthenticated(), IsVendorOrAdmin()]
        # Update/Delete: Only admin
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUserType()]
        # Default: authenticated
        return [IsAuthenticated()]
    
class VendorProductViewSet(viewsets.ModelViewSet):
    queryset = VendorProduct.objects.all()
    serializer_class = VendorProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated(), IsVendorOrAdmin()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUserType()]
        return [IsAuthenticated()]
    


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
    


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
    

class SubscriptionBoxViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionBox.objects.all()
    serializer_class = SubscriptionBoxSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

class ScheduledItemViewSet(viewsets.ModelViewSet):
    queryset = ScheduledItem.objects.all()
    serializer_class = ScheduledItemSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
    
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
