from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'price', 'stock')
    # Cho phép lọc danh sách theo tác giả
    list_filter = ('author',)
    search_fields = ('title', 'author')