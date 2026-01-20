from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Cart, CartItem
from .serializers import (
    CartSerializer, CartItemSerializer, 
    AddToCartSerializer, UpdateCartItemSerializer
)
from .services import BookServiceClient


class CartView(APIView):
    """API endpoint to view cart"""
    permission_classes = [AllowAny]

    def get(self, request):
        customer_id = request.query_params.get('customer_id')
        
        if not customer_id:
            return Response({
                'error': 'customer_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            customer_id = int(customer_id)
        except ValueError:
            return Response({
                'error': 'Invalid customer_id'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get or create cart for customer
        cart, created = Cart.objects.get_or_create(customer_id=customer_id)

        # Fetch book details for all items
        book_service = BookServiceClient()
        book_ids = [item.book_id for item in cart.items.all()]
        books = book_service.get_books_by_ids(book_ids)
        book_details = {book['id']: book for book in books}

        # Serialize cart with book details
        serializer = CartSerializer(cart, context={'book_details': book_details})
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddToCartView(APIView):
    """API endpoint to add items to cart"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        customer_id = serializer.validated_data['customer_id']
        book_id = serializer.validated_data['book_id']
        quantity = serializer.validated_data['quantity']

        # Check if book exists and has sufficient stock
        book_service = BookServiceClient()
        book = book_service.get_book(book_id)
        
        if not book:
            return Response({
                'error': 'Book not found'
            }, status=status.HTTP_404_NOT_FOUND)

        stock_info = book_service.check_stock(book_id, quantity)
        if not stock_info or not stock_info.get('available'):
            return Response({
                'error': 'Insufficient stock',
                'available_stock': book.get('stock', 0)
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get or create cart
        cart, created = Cart.objects.get_or_create(customer_id=customer_id)

        # Check if item already exists in cart
        try:
            cart_item = CartItem.objects.get(cart=cart, book_id=book_id)
            # Update quantity
            new_quantity = cart_item.quantity + quantity
            
            # Check stock for new quantity
            stock_check = book_service.check_stock(book_id, new_quantity)
            if not stock_check or not stock_check.get('available'):
                return Response({
                    'error': 'Insufficient stock for requested quantity',
                    'current_in_cart': cart_item.quantity,
                    'available_stock': book.get('stock', 0)
                }, status=status.HTTP_400_BAD_REQUEST)
            
            cart_item.quantity = new_quantity
            cart_item.save()
            message = 'Cart item quantity updated'
        except CartItem.DoesNotExist:
            # Create new cart item
            cart_item = CartItem.objects.create(
                cart=cart,
                book_id=book_id,
                quantity=quantity,
                price_at_add=book['price']
            )
            message = 'Item added to cart'

        # Return updated cart
        book_details = {book['id']: book}
        cart_serializer = CartSerializer(cart, context={'book_details': book_details})
        
        return Response({
            'message': message,
            'cart': cart_serializer.data
        }, status=status.HTTP_201_CREATED)


class UpdateCartItemView(APIView):
    """API endpoint to update cart item quantity"""
    permission_classes = [AllowAny]

    def put(self, request, item_id):
        serializer = UpdateCartItemSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        quantity = serializer.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(id=item_id)
        except CartItem.DoesNotExist:
            return Response({
                'error': 'Cart item not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # Check stock availability
        book_service = BookServiceClient()
        stock_info = book_service.check_stock(cart_item.book_id, quantity)
        
        if not stock_info or not stock_info.get('available'):
            return Response({
                'error': 'Insufficient stock',
                'available_stock': stock_info.get('stock', 0) if stock_info else 0
            }, status=status.HTTP_400_BAD_REQUEST)

        cart_item.quantity = quantity
        cart_item.save()

        # Get book details
        book = book_service.get_book(cart_item.book_id)
        book_details = {book['id']: book} if book else {}
        
        item_serializer = CartItemSerializer(cart_item, context={'book_details': book_details})
        
        return Response({
            'message': 'Cart item updated',
            'item': item_serializer.data
        }, status=status.HTTP_200_OK)


class RemoveCartItemView(APIView):
    """API endpoint to remove item from cart"""
    permission_classes = [AllowAny]

    def delete(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id)
            cart_item.delete()
            
            return Response({
                'message': 'Item removed from cart'
            }, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({
                'error': 'Cart item not found'
            }, status=status.HTTP_404_NOT_FOUND)


class ClearCartView(APIView):
    """API endpoint to clear all items from cart"""
    permission_classes = [AllowAny]

    def delete(self, request):
        customer_id = request.query_params.get('customer_id')
        
        if not customer_id:
            return Response({
                'error': 'customer_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            customer_id = int(customer_id)
        except ValueError:
            return Response({
                'error': 'Invalid customer_id'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = Cart.objects.get(customer_id=customer_id)
            cart.items.all().delete()
            
            return Response({
                'message': 'Cart cleared successfully'
            }, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({
                'message': 'Cart is already empty'
            }, status=status.HTTP_200_OK)
