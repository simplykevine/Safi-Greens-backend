from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='phone_number')
    pin = serializers.CharField(write_only=True, min_length=4, max_length=20)

    class Meta:
        model = User
        fields = ['phone', 'name', 'user_type', 'pin']

    def validate_phone(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("A user with this phone number already exists.")
        return value

    def create(self, validated_data):
        pin = validated_data.pop('pin')
        phone_number = validated_data.pop('phone_number')
        return User.objects.create_user(phone_number=phone_number, password=pin, **validated_data)

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    pin = serializers.CharField(write_only=True)
    
    def validate(self, data):
        phone = data.get('phone')
        pin = data.get('pin')
        user = authenticate(phone_number=phone, password=pin)
        if not user:
            raise serializers.ValidationError("Invalid phone or pin")
        if not user.is_active:
            raise serializers.ValidationError("User is inactive")
        data['user'] = user
        return data