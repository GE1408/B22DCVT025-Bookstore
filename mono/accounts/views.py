from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomerRegistrationForm
from .models import Customer

# View Đăng ký
def register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Đăng ký thành công! Hãy đăng nhập.")
            return redirect('login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

# View Đăng nhập (Đơn giản hóa cho bản Monolith)
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            customer = Customer.objects.get(email=email, password=password)
            request.session['customer_id'] = customer.id # Lưu session
            return redirect('book_list') # Chuyển đến danh mục sách
        except Customer.DoesNotExist:
            messages.error(request, "Email hoặc mật khẩu không đúng")
    return render(request, 'accounts/login.html')