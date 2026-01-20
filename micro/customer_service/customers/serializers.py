from rest_framework import serializers
from .models import Customer
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model (read-only, no password)"""
    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'full_name', 'phone', 'address', 'created_at']
        read_only_fields = ['id', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for customer registration"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = Customer
        fields = ['username', 'email', 'password', 'password_confirm', 'full_name', 'phone', 'address']

    def validate(self, attrs):
        """Validate password match"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        
        # Validate password strength
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        
        return attrs

    def create(self, validated_data):
        """Create customer with hashed password"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        customer = Customer(**validated_data)
        customer.set_password(password)
        customer.save()
        
        return customer


class LoginSerializer(serializers.Serializer):
    """Serializer for customer login"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
