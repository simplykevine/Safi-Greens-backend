from django.db import models
from product.models import Product 
from users.models import User

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    customer = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.customer.type != 'customer':
            raise ValueError("Only users with type 'customer' can have a cart.")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Cart for {self.customer.name}"
        
class CartItem(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart_id.customer.name}'s cart"