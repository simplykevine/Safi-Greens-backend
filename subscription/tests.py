from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models import User
from product.models import Product
from .models import SubscriptionBox, ScheduledItem


class SubscriptionBoxModelTest(TestCase):
    def setUp(self):
        self.buyer = User.objects.create(
            name='Buyer One', type='customer'
        )
        self.vendor = User.objects.create(
            name='Vendor One', type='vendor'
        )
    
        self.product = Product.objects.create(
            name='Carrot'
        )

    def test_subscription_box_creation(self):
        sub_box = SubscriptionBox.objects.create(
            buyer=self.buyer,
            vendor=self.vendor,
            name="Weekly Veggie Box",
            frequency="weekly",
            price=100,
            status="active"
        )
        self.assertEqual(str(sub_box), f"Subscription Weekly Veggie Box for {self.buyer.name}")
        self.assertEqual(sub_box.buyer.type, 'customer')
        self.assertEqual(sub_box.vendor.type, 'vendor')

    def test_subscription_box_with_invalid_buyer_vendor(self):
        vendor_user = User.objects.create(
            name='Not a Buyer', type='vendor'
        )
        with self.assertRaises(ValidationError):
            box = SubscriptionBox(
                buyer=vendor_user, vendor=self.vendor, name="Test", frequency="weekly", price=100, status="active"
            )
            box.full_clean()

        customer_user = User.objects.create(
            name='Not a Vendor', type='customer'
        )
        with self.assertRaises(ValidationError):
            box = SubscriptionBox(
                buyer=self.buyer, vendor=customer_user, name="Test", frequency="weekly", price=100, status="active"
            )
            box.full_clean()

    def test_scheduled_item_creation(self):
        sub_box = SubscriptionBox.objects.create(
            buyer=self.buyer,
            vendor=self.vendor,
            name="Weekly Veggie Box",
            frequency="weekly",
            price=100,
            status="active"
        )
        scheduled_item = ScheduledItem.objects.create(
            product=self.product,
            schedule=sub_box,
            price_per_unit=5.00,
            quantity=2,
            unit='kg'
        )
        self.assertEqual(str(scheduled_item),
                         f"2kg {self.product.name} (Schedule {sub_box.schedule_id})")
        self.assertEqual(scheduled_item.schedule, sub_box)
        self.assertEqual(scheduled_item.product, self.product)