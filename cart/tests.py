from django.test import TestCase
from users.models import User
from product.models import Product
from cart.models import Cart, CartItem
class CartModelTest(TestCase):
    def setUp(self):
        self.customer = User.objects.create(name="Test Customer", type="customer")
        self.product = Product.objects.create(
            name="Test Product",
            category="Test Category",
            unit="kg"
        )
    def test_create_cart(self):
        cart = Cart.objects.create(customer=self.customer)
        self.assertEqual(cart.customer, self.customer)
        self.assertIsNotNone(cart.created_at)
    def test_cart_str(self):
        cart = Cart.objects.create(customer=self.customer)
        self.assertIn(self.customer.name, str(cart))
    def test_create_cartitem(self):
        cart = Cart.objects.create(customer=self.customer)
        cart_item = CartItem.objects.create(cart_id=cart, product=self.product, quantity=3)
        self.assertEqual(cart_item.cart_id, cart)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 3)
        self.assertIsNotNone(cart_item.added_at)
    def test_cartitem_str(self):
        cart = Cart.objects.create(customer=self.customer)
        cart_item = CartItem.objects.create(cart_id=cart, product=self.product, quantity=2)
        self.assertIn(self.product.name, str(cart_item))
        self.assertIn(self.customer.name, str(cart_item))
