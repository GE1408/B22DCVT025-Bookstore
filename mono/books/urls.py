from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.book_list, name='book_list'), # Tên này phải khớp với redirect trong login
]