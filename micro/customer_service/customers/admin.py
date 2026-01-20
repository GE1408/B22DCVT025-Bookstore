from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'full_name', 'created_at']
    search_fields = ['username', 'email', 'full_name']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
