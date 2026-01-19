from django.contrib import admin
from .models import Cart, CartItem

# Cách hiển thị các món hàng nằm ngay trong trang chi tiết giỏ hàng
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1 # Số dòng trống hiện ra để thêm nhanh hàng mới

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'created_at')
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'book', 'quantity')