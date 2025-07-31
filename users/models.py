from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, user_type='customer', name=None, **extra_fields):
        if not phone_number:
            raise ValueError("Users must have a phone number")
        user = self.model(phone_number=phone_number, user_type=user_type, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, user_type="admin", name=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, user_type, name, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('vendor', 'Vendor'),
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    )
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    profile_picture = models.ImageField(upload_to='users/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    shop_name = models.CharField(max_length=100, blank=True, null=True)
    till_number = models.IntegerField(blank=True, null=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['user_type', 'name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.name} ({self.user_type})"