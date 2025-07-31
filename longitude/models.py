from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)  # Mama Mboga or customer name
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_mama_mboga = models.BooleanField(default=False)  # True for Mama Mboga, False for Customer
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({'Mama Mboga' if self.is_mama_mboga else 'Customer'})"