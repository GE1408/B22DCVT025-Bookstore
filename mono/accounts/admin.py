from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # Hiển thị các cột thông tin ra bảng danh sách
    list_display = ('id', 'name', 'email')
    # Thêm thanh tìm kiếm theo tên và email
    search_fields = ('name', 'email')