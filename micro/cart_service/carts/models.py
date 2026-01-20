from django.db import models


class Cart(models.Model):
    """Cart model for customer shopping cart"""
    customer_id = models.IntegerField()  # Reference to customer from Customer Service
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'
        ordering = ['-created_at']

    def __str__(self):
        return f"Cart for Customer {self.customer_id}"

    def get_total(self):
        """Calculate total price of all items in cart"""
        return sum(item.get_subtotal() for item in self.items.all())

    def get_item_count(self):
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Cart item model"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book_id = models.IntegerField()  # Reference to book from Book Service
    quantity = models.IntegerField(default=1)
    price_at_add = models.DecimalField(max_digits=10, decimal_places=2)  # Price when added to cart
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart_items'
        ordering = ['-created_at']
        unique_together = ['cart', 'book_id']  # Prevent duplicate books in same cart

    def __str__(self):
        return f"Book {self.book_id} x{self.quantity}"

    def get_subtotal(self):
        """Calculate subtotal for this item"""
        return self.price_at_add * self.quantity
