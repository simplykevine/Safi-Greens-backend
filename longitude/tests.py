from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from .models import Location

class LocationAPITests(APITestCase):
    def setUp(self):
        self.create_url = reverse('create_location')
        self.nearby_url = reverse('nearby_mama_mbogas')

    @patch('longitude.views.reverse_geocode', return_value="Test Address, Nairobi, Kenya")
    def test_create_mama_mboga(self, mock_reverse):
        data = {
            "name": "Mama Aisha",
            "latitude": -1.2921,
            "longitude": 36.8219,
            "is_mama_mboga": True
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)
        loc = Location.objects.first()
        self.assertEqual(loc.name, "Mama Aisha")
        self.assertEqual(loc.address, "Test Address, Nairobi, Kenya")

    @patch('longitude.views.reverse_geocode', return_value="Customer Address, Nairobi, Kenya")
    def test_create_customer(self, mock_reverse):
        data = {
            "name": "Customer Kim",
            "latitude": -1.2950,
            "longitude": 36.8200,
            "is_mama_mboga": False
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)
        loc = Location.objects.first()
        self.assertEqual(loc.is_mama_mboga, False)
        self.assertEqual(loc.address, "Customer Address, Nairobi, Kenya")

    @patch('longitude.views.reverse_geocode', return_value="Test Address")
    def test_list_locations(self, mock_reverse):
        # Create two locations
        self.client.post(self.create_url, {
            "name": "Mama Aisha",
            "latitude": -1.2921,
            "longitude": 36.8219,
            "is_mama_mboga": True
        }, format='json')
        self.client.post(self.create_url, {
            "name": "Customer Kim",
            "latitude": -1.2950,
            "longitude": 36.8200,
            "is_mama_mboga": False
        }, format='json')
        # List all
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    @patch('longitude.views.reverse_geocode', return_value="Test Address")
    def test_nearby_mama_mbogas(self, mock_reverse):
        # Add a mama mboga
        self.client.post(self.create_url, {
            "name": "Mama Aisha",
            "latitude": -1.2921,
            "longitude": 36.8219,
            "is_mama_mboga": True
        }, format='json')
        # Add a customer
        self.client.post(self.create_url, {
            "name": "Customer Kim",
            "latitude": -1.2930,
            "longitude": 36.8220,
            "is_mama_mboga": False
        }, format='json')
        # Search near customer location
        params = {
            "latitude": -1.2930,
            "longitude": 36.8220,
            "radius": 1  # miles
        }
        response = self.client.get(self.nearby_url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Mama Aisha")
        self.assertIn("distance_miles", response.data[0])

    def test_nearby_mama_mbogas_invalid_params(self):
        response = self.client.get(self.nearby_url, {"latitude": "bad", "longitude": "bad"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)