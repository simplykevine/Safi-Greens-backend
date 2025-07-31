from django.test import TestCase
from .models import User

class TestUserModel(TestCase):
    def test_create_customer(self):
        user = User.objects.create(
            name="Test Customer",
            phone_number="0711111111",
            password_hash="hash1",
            location="Kigali",
            type="customer"
        )
        self.assertIsNotNone(user.pk)
        self.assertEqual(user.type, "customer")
        self.assertIsNone(user.shop_name)
        self.assertIsNone(user.till_number)
        self.assertIn("Customer", str(user))

    def test_create_vendor(self):
        vendor = User.objects.create(
            name="Test Vendor",
            phone_number="0722222222",
            password_hash="hash2",
            location="Kampala",
            type="vendor",
            shop_name="Mama Mboga",
            till_number=123456
        )
        self.assertIsNotNone(vendor.pk)
        self.assertEqual(vendor.type, "vendor")
        self.assertEqual(vendor.shop_name, "Mama Mboga")
        self.assertEqual(vendor.till_number, 123456)
        self.assertIn("Vendor", str(vendor))

    def test_vendor_unique_till_number(self):
        User.objects.create(
            name="Vendor A",
            phone_number="0733333333",
            password_hash="hash3",
            location="Nairobi",
            type="vendor",
            shop_name="Veggies",
            till_number=222222
        )
        with self.assertRaises(Exception):
            User.objects.create(
                name="Vendor B",
                phone_number="0744444444",
                password_hash="hash4",
                location="Nairobi",
                type="vendor",
                shop_name="Fruits",
                till_number=222222  # Should fail: not unique
            )

    def test_str_method(self):
        user = User.objects.create(
            name="Alice",
            phone_number="0755555555",
            password_hash="hash5",
            location="Mombasa",
            type="customer"
        )
        vendor = User.objects.create(
            name="Bob",
            phone_number="0766666666",
            password_hash="hash6",
            location="Mombasa",
            type="vendor",
            shop_name="Bob's Greens",
            till_number=987654
        )
        self.assertEqual(str(user), "Alice (Customer (Buyer))")
        self.assertEqual(str(vendor), "Bob (Vendor (Mama Mboga))")