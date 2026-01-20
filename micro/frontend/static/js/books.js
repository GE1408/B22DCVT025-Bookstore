// Book Catalog Management
let allBooks = [];
let filteredBooks = [];
let selectedCategory = 'all';

// Load and display books
async function loadBooks() {
    const booksGrid = document.getElementById('booksGrid');
    UI.showLoading(booksGrid);

    try {
        const filters = {};
        if (selectedCategory !== 'all') {
            filters.category = selectedCategory;
        }

        allBooks = await api.getBooks(filters);
        filteredBooks = allBooks;
        displayBooks(filteredBooks);
    } catch (error) {
        booksGrid.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📚</div>
                <h2>Failed to load books</h2>
                <p>${error.message}</p>
            </div>
        `;
        UI.showToast('Failed to load books', 'error');
    }
}

// Display books in grid
function displayBooks(books) {
    const booksGrid = document.getElementById('booksGrid');

    if (books.length === 0) {
        booksGrid.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📚</div>
                <h2>No books found</h2>
                <p>Try adjusting your search or filters</p>
            </div>
        `;
        return;
    }

    booksGrid.innerHTML = books.map(book => `
        <div class="glass-card book-card" data-book-id="${book.id}">
            <div class="book-image">
                <img src="${book.image_url || 'https://via.placeholder.com/280x350/667eea/ffffff?text=' + encodeURIComponent(book.title)}" 
                     alt="${book.title}"
                     onerror="this.src='https://via.placeholder.com/280x350/667eea/ffffff?text=' + encodeURIComponent('${book.title}')">
                <span class="stock-badge ${book.in_stock ? 'in-stock' : 'out-of-stock'}">
                    ${book.in_stock ? `${book.stock} in stock` : 'Out of stock'}
                </span>
            </div>
            <div class="book-info">
                <h3>${book.title}</h3>
                <p class="book-author">by ${book.author}</p>
                <span class="book-category">${book.category}</span>
                <div class="book-price">${UI.formatCurrency(book.price)}</div>
                <button class="btn btn-primary" 
                        onclick="addToCart(${book.id})"
                        ${!book.in_stock ? 'disabled' : ''}>
                    ${book.in_stock ? '🛒 Add to Cart' : 'Out of Stock'}
                </button>
            </div>
        </div>
    `).join('');
}

// Add book to cart
async function addToCart(bookId) {
    const customer = auth.getCustomer();

    if (!customer) {
        UI.showToast('Please login to add items to cart', 'error');
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 1500);
        return;
    }

    try {
        const result = await api.addToCart({
            customer_id: customer.id,
            book_id: bookId,
            quantity: 1
        });

        UI.showToast(result.message || 'Added to cart!', 'success');
        UI.updateCartBadge();
    } catch (error) {
        UI.showToast(error.message || 'Failed to add to cart', 'error');
    }
}

// Search books
function searchBooks(query) {
    const searchTerm = query.toLowerCase();
    filteredBooks = allBooks.filter(book =>
        book.title.toLowerCase().includes(searchTerm) ||
        book.author.toLowerCase().includes(searchTerm) ||
        book.category.toLowerCase().includes(searchTerm)
    );
    displayBooks(filteredBooks);
}

// Filter by category
function filterByCategory(category) {
    selectedCategory = category;

    // Update active filter button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');

    loadBooks();
}

// Initialize books page
document.addEventListener('DOMContentLoaded', () => {
    // Load books if on index page
    if (document.getElementById('booksGrid')) {
        loadBooks();

        // Setup search
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                searchBooks(e.target.value);
            });
        }
    }
});
