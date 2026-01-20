from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['price_at_add', 'created_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_id', 'get_item_count', 'get_total', 'created_at']
    search_fields = ['customer_id']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CartItemInline]

    def get_item_count(self, obj):
        return obj.get_item_count()
    get_item_count.short_description = 'Items'

    def get_total(self, obj):
        return f"${obj.get_total():.2f}"
    get_total.short_description = 'Total'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'book_id', 'quantity', 'price_at_add', 'get_subtotal', 'created_at']
    search_fields = ['cart__customer_id', 'book_id']
    list_filter = ['created_at']
    readonly_fields = ['price_at_add', 'created_at', 'updated_at']

    def get_subtotal(self, obj):
        return f"${obj.get_subtotal():.2f}"
    get_subtotal.short_description = 'Subtotal'
