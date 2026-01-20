// API Client for Microservices
class APIClient {
    constructor() {
        this.customerAPI = 'http://localhost:8001/api';
        this.bookAPI = 'http://localhost:8002/api';
        this.cartAPI = 'http://localhost:8003/api';
    }

    // Helper method for making requests
    async request(url, options = {}) {
        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || data.message || 'Request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Customer Service APIs
    async register(userData) {
        return this.request(`${this.customerAPI}/register/`, {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    async login(credentials) {
        return this.request(`${this.customerAPI}/login/`, {
            method: 'POST',
            body: JSON.stringify(credentials)
        });
    }

    async getCustomerProfile(customerId) {
        return this.request(`${this.customerAPI}/profile/${customerId}/`);
    }

    async getAllCustomers() {
        return this.request(`${this.customerAPI}/customers/`);
    }

    // Book Service APIs
    async getBooks(filters = {}) {
        const params = new URLSearchParams(filters);
        const url = `${this.bookAPI}/books/${params.toString() ? '?' + params.toString() : ''}`;
        return this.request(url);
    }

    async getBook(bookId) {
        return this.request(`${this.bookAPI}/books/${bookId}/`);
    }

    async createBook(bookData) {
        return this.request(`${this.bookAPI}/books/create/`, {
            method: 'POST',
            body: JSON.stringify(bookData)
        });
    }

    async checkStock(bookId, quantity) {
        return this.request(`${this.bookAPI}/books/${bookId}/check-stock/?quantity=${quantity}`);
    }

    // Cart Service APIs
    async getCart(customerId) {
        return this.request(`${this.cartAPI}/cart/?customer_id=${customerId}`);
    }

    async addToCart(cartData) {
        return this.request(`${this.cartAPI}/cart/add/`, {
            method: 'POST',
            body: JSON.stringify(cartData)
        });
    }

    async updateCartItem(itemId, quantity) {
        return this.request(`${this.cartAPI}/cart/update/${itemId}/`, {
            method: 'PUT',
            body: JSON.stringify({ quantity })
        });
    }

    async removeFromCart(itemId) {
        return this.request(`${this.cartAPI}/cart/remove/${itemId}/`, {
            method: 'DELETE'
        });
    }

    async clearCart(customerId) {
        return this.request(`${this.cartAPI}/cart/clear/?customer_id=${customerId}`, {
            method: 'DELETE'
        });
    }
}

// Create global API client instance
const api = new APIClient();
