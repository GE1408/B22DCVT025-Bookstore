from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for CartItem model"""
    subtotal = serializers.SerializerMethodField()
    book_details = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'book_id', 'quantity', 'price_at_add', 'subtotal', 'book_details', 'created_at']
        read_only_fields = ['id', 'price_at_add', 'created_at']

    def get_subtotal(self, obj):
        """Calculate subtotal for this item"""
        return float(obj.get_subtotal())

    def get_book_details(self, obj):
        """Get book details from context (passed from view)"""
        book_details = self.context.get('book_details', {})
        return book_details.get(obj.book_id, None)


class CartSerializer(serializers.ModelSerializer):
    """Serializer for Cart model"""
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'customer_id', 'items', 'total', 'item_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_total(self, obj):
        """Calculate cart total"""
        return float(obj.get_total())

    def get_item_count(self, obj):
        """Get total item count"""
        return obj.get_item_count()


class AddToCartSerializer(serializers.Serializer):
    """Serializer for adding items to cart"""
    customer_id = serializers.IntegerField(required=True)
    book_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True, min_value=1)

    def validate_quantity(self, value):
        """Validate quantity is positive"""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value


class UpdateCartItemSerializer(serializers.Serializer):
    """Serializer for updating cart item quantity"""
    quantity = serializers.IntegerField(required=True, min_value=1)

    def validate_quantity(self, value):
        """Validate quantity is positive"""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value
