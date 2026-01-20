// Authentication Manager
class AuthManager {
    constructor() {
        this.storageKey = 'bookstore_auth';
    }

    // Save authentication data
    saveAuth(authData) {
        localStorage.setItem(this.storageKey, JSON.stringify(authData));
    }

    // Get authentication data
    getAuth() {
        const data = localStorage.getItem(this.storageKey);
        return data ? JSON.parse(data) : null;
    }

    // Get access token
    getAccessToken() {
        const auth = this.getAuth();
        return auth?.tokens?.access || null;
    }

    // Get current customer
    getCustomer() {
        const auth = this.getAuth();
        return auth?.customer || null;
    }

    // Check if user is authenticated
    isAuthenticated() {
        return this.getCustomer() !== null;
    }

    // Logout
    logout() {
        localStorage.removeItem(this.storageKey);
        window.location.href = 'login.html';
    }

    // Update customer info
    updateCustomer(customerData) {
        const auth = this.getAuth();
        if (auth) {
            auth.customer = { ...auth.customer, ...customerData };
            this.saveAuth(auth);
        }
    }
}

// Create global auth manager instance
const auth = new AuthManager();

// UI Helper Functions
const UI = {
    // Show toast notification
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'slideIn 0.3s ease-out reverse';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    },

    // Show loading spinner
    showLoading(element) {
        element.innerHTML = `
            <div class="loading-container">
                <div class="loading"></div>
            </div>
        `;
    },

    // Update navigation based on auth status
    updateNav() {
        const navLinks = document.querySelector('.nav-links');
        const customer = auth.getCustomer();

        if (customer) {
            const cartLink = navLinks.querySelector('a[href="cart.html"]');
            if (cartLink) {
                const badge = cartLink.querySelector('.badge');
                // Update cart badge count
                this.updateCartBadge();
            }

            // Update user info in nav
            const userInfo = navLinks.querySelector('.user-info');
            if (userInfo) {
                userInfo.textContent = customer.full_name || customer.username;
            }
        }
    },

    // Update cart badge count
    async updateCartBadge() {
        const customer = auth.getCustomer();
        if (!customer) return;

        try {
            const cartData = await api.getCart(customer.id);
            const badge = document.querySelector('.cart-badge .badge');
            if (badge && cartData.item_count) {
                badge.textContent = cartData.item_count;
                badge.style.display = 'flex';
            }
        } catch (error) {
            console.error('Error updating cart badge:', error);
        }
    },

    // Format currency
    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    },

    // Format date
    formatDate(dateString) {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    UI.updateNav();
});
