from django.urls import path
from .views import RegisterView, LoginView, CustomerProfileView, CustomerListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/<int:customer_id>/', CustomerProfileView.as_view(), name='profile'),
    path('customers/', CustomerListView.as_view(), name='customer-list'),
]
