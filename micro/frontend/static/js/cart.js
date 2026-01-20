// Cart Management
let currentCart = null;

// Load cart
async function loadCart() {
    const customer = auth.getCustomer();

    if (!customer) {
        window.location.href = 'login.html';
        return;
    }

    const cartItems = document.getElementById('cartItems');
    UI.showLoading(cartItems);

    try {
        currentCart = await api.getCart(customer.id);
        displayCart(currentCart);
    } catch (error) {
        cartItems.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🛒</div>
                <h2>Failed to load cart</h2>
                <p>${error.message}</p>
            </div>
        `;
        UI.showToast('Failed to load cart', 'error');
    }
}

// Display cart
function displayCart(cart) {
    const cartItems = document.getElementById('cartItems');
    const cartSummary = document.getElementById('cartSummary');

    if (!cart.items || cart.items.length === 0) {
        cartItems.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🛒</div>
                <h2>Your cart is empty</h2>
                <p>Add some books to get started!</p>
                <a href="index.html" class="btn btn-primary">Browse Books</a>
            </div>
        `;
        cartSummary.innerHTML = '';
        return;
    }

    // Display cart items
    cartItems.innerHTML = cart.items.map(item => `
        <div class="glass-card cart-item" data-item-id="${item.id}">
            <div class="cart-item-image">
                <img src="${item.book_details?.image_url || 'https://via.placeholder.com/100x150/667eea/ffffff?text=Book'}" 
                     alt="${item.book_details?.title || 'Book'}">
            </div>
            <div class="cart-item-info">
                <h3 class="cart-item-title">${item.book_details?.title || 'Unknown Book'}</h3>
                <p class="cart-item-author">by ${item.book_details?.author || 'Unknown Author'}</p>
                <p class="cart-item-price">${UI.formatCurrency(item.price_at_add)} each</p>
            </div>
            <div class="quantity-controls">
                <button class="quantity-btn" onclick="updateQuantity(${item.id}, ${item.quantity - 1})">-</button>
                <div class="quantity-display">${item.quantity}</div>
                <button class="quantity-btn" onclick="updateQuantity(${item.id}, ${item.quantity + 1})">+</button>
            </div>
            <div>
                <div class="cart-item-price">${UI.formatCurrency(item.subtotal)}</div>
                <button class="btn btn-danger" onclick="removeItem(${item.id})" style="margin-top: 0.5rem;">
                    🗑️ Remove
                </button>
            </div>
        </div>
    `).join('');

    // Display cart summary
    cartSummary.innerHTML = `
        <h2>Cart Summary</h2>
        <div style="margin: 1.5rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span>Items:</span>
                <span>${cart.item_count}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                <span>Subtotal:</span>
                <span>${UI.formatCurrency(cart.total)}</span>
            </div>
            <hr style="border: 1px solid rgba(148, 163, 184, 0.2); margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 1.5rem;">
                <strong>Total:</strong>
                <strong class="cart-total">${UI.formatCurrency(cart.total)}</strong>
            </div>
        </div>
        <button class="btn btn-primary" style="width: 100%; margin-bottom: 0.5rem;">
            💳 Proceed to Checkout
        </button>
        <button class="btn btn-outline" onclick="clearCart()" style="width: 100%;">
            🗑️ Clear Cart
        </button>
    `;

    UI.updateCartBadge();
}

// Update item quantity
async function updateQuantity(itemId, newQuantity) {
    if (newQuantity < 1) {
        removeItem(itemId);
        return;
    }

    try {
        await api.updateCartItem(itemId, newQuantity);
        UI.showToast('Quantity updated', 'success');
        await loadCart(); // Reload cart
    } catch (error) {
        UI.showToast(error.message || 'Failed to update quantity', 'error');
    }
}

// Remove item from cart
async function removeItem(itemId) {
    if (!confirm('Remove this item from cart?')) {
        return;
    }

    try {
        await api.removeFromCart(itemId);
        UI.showToast('Item removed from cart', 'success');
        await loadCart(); // Reload cart
    } catch (error) {
        UI.showToast(error.message || 'Failed to remove item', 'error');
    }
}

// Clear cart
async function clearCart() {
    if (!confirm('Clear all items from cart?')) {
        return;
    }

    const customer = auth.getCustomer();
    try {
        await api.clearCart(customer.id);
        UI.showToast('Cart cleared', 'success');
        await loadCart(); // Reload cart
    } catch (error) {
        UI.showToast(error.message || 'Failed to clear cart', 'error');
    }
}

// Initialize cart page
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('cartItems')) {
        loadCart();
    }
});
