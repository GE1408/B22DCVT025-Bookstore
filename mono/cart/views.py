from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cart, CartItem
from books.models import Book
from accounts.models import Customer

# Hàm hiển thị giỏ hàng (Cần phải có để hết lỗi AttributeError)
def view_cart(request):
    customer_id = request.session.get('customer_id')
    cart = Cart.objects.filter(customer_id=customer_id).first()
    return render(request, 'cart/view_cart.html', {'cart': cart})

# Hàm thêm vào giỏ hàng (Đã sửa để không nhảy trang)
def add_to_cart(request, book_id):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.error(request, "Vui lòng đăng nhập để mua hàng.")
        return redirect('login')
    
    customer = get_object_or_404(Customer, id=customer_id)
    book = get_object_or_404(Book, id=book_id)
    
    if book.stock > 0:
        cart, _ = Cart.objects.get_or_create(customer=customer)
        item, created = CartItem.objects.get_or_create(cart=cart, book=book)
        if not created:
            item.quantity += 1
        item.save()
        
        # Gửi thông báo thành công
        messages.success(request, f"Đã thêm '{book.title}' vào giỏ hàng!")
    else:
        messages.error(request, "Sách này đã hết hàng!")

    # QUAN TRỌNG: Điều hướng ngược lại trang danh sách sách thay vì view_cart
    return redirect('book_list')

def remove_from_cart(request, item_id):
    # Lấy item cụ thể dựa trên ID
    item = get_object_or_404(CartItem, id=item_id)
    
    # Kiểm tra quyền (chỉ cho phép xóa nếu đúng giỏ hàng của user đó)
    customer_id = request.session.get('customer_id')
    if item.cart.customer.id == customer_id:
        item.delete()
        messages.warning(request, f"Đã xóa '{item.book.title}' khỏi giỏ hàng.")
    
    return redirect('view_cart')