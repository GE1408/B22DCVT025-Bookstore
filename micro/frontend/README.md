# Professional Web UI - Microservices Book Store

## 🎨 UI Overview

Đã tạo xong **giao diện web chuyên nghiệp** với thiết kế hiện đại cho hệ thống microservices!

### ✨ Design Features

- **Dark Theme** với vibrant gradient colors
- **Glassmorphism effects** cho cards và modals
- **Smooth animations** và transitions
- **Responsive design** (mobile-first approach)
- **Modern typography** với Google Fonts (Inter)
- **Micro-interactions** cho better UX

---

## 📁 Frontend Structure

```
frontend/
├── index.html              ✅ Homepage/Book Catalog
├── login.html              ✅ Login Page
├── register.html           ✅ Registration Page
├── cart.html               ✅ Shopping Cart Page
├── server.py               ✅ Python HTTP Server
├── static/
│   ├── css/
│   │   └── style.css       ✅ Complete Design System
│   └── js/
│       ├── api.js          ✅ API Client (all 3 services)
│       ├── auth.js         ✅ Authentication Manager
│       ├── books.js        ✅ Book Catalog Logic
│       └── cart.js         ✅ Shopping Cart Logic
```

**Total: 9 files created**

---

## 🌐 Pages Overview

### 1. Homepage (index.html)

**URL**: `http://localhost:8000/index.html`

**Features**:
- Hero section với gradient heading
- Search bar (tìm kiếm theo title, author, category)
- Category filter buttons (All, Programming, Python, JavaScript, Computer Science)
- Book grid với glassmorphism cards
- Book cards hiển thị:
  - Book image (với fallback placeholder)
  - Title, author, category
  - Price với currency formatting
  - Stock badge (in stock / out of stock)
  - "Add to Cart" button

**Design**:
- Animated gradient background
- Sticky header với glassmorphism
- Responsive grid (auto-fill minmax 280px)
- Hover effects trên book cards
- Smooth scroll animations

### 2. Login Page (login.html)

**URL**: `http://localhost:8000/login.html`

**Features**:
- Username và password fields
- Form validation
- JWT token storage
- Auto-redirect nếu đã login
- Link to registration page

**Design**:
- Centered glassmorphism card
- Animated gradient background
- Modern input fields
- Loading state on submit

### 3. Registration Page (register.html)

**URL**: `http://localhost:8000/register.html`

**Features**:
- Fields: username, email, full_name, phone, address, password, password_confirm
- Real-time password confirmation validation
- Form validation (required fields, email format, min length)
- Success redirect to login

**Design**:
- Consistent với login page
- Form error messages
- Disabled state on submit

### 4. Shopping Cart Page (cart.html)

**URL**: `http://localhost:8000/cart.html`

**Features**:
- Cart items với book details (từ Book Service)
- Quantity controls (+/- buttons)
- Remove item button
- Cart summary với total calculation
- Empty cart state
- Clear cart button
- Checkout button (placeholder)

**Design**:
- Two-column layout (items + summary)
- Responsive (single column on mobile)
- Cart item cards với image
- Sticky cart summary
- Real-time total updates

---

## 🎨 Design System

### Color Palette

```css
--primary: #6366f1       /* Indigo */
--secondary: #ec4899     /* Pink */
--accent: #10b981        /* Green */
--dark: #0f172a          /* Slate 900 */
--dark-light: #1e293b    /* Slate 800 */
--text: #f1f5f9          /* Slate 100 */
--text-muted: #94a3b8    /* Slate 400 */
```

### Gradients

- **Primary**: Purple to Violet
- **Secondary**: Pink to Red
- **Accent**: Blue to Cyan
- **Background**: Animated radial gradients

### Components

- **Glass Cards**: backdrop-filter blur + rgba background
- **Buttons**: Gradient backgrounds, hover lift effects
- **Inputs**: Dark background, focus ring
- **Toast Notifications**: Slide-in animation, auto-dismiss
- **Loading Spinner**: Rotating border animation

### Typography

- **Font Family**: Inter (Google Fonts)
- **Headings**: 700-800 weight
- **Body**: 400-500 weight
- **Sizes**: Responsive scale

---

## 🔌 API Integration

### API Client (api.js)

All API calls được handle thông qua `APIClient` class:

**Customer Service**:
- `register(userData)` - Đăng ký
- `login(credentials)` - Đăng nhập
- `getCustomerProfile(id)` - Lấy profile
- `getAllCustomers()` - List customers

**Book Service**:
- `getBooks(filters)` - List books với filters
- `getBook(id)` - Chi tiết sách
- `createBook(data)` - Tạo sách mới
- `checkStock(id, quantity)` - Kiểm tra tồn kho

**Cart Service**:
- `getCart(customerId)` - Lấy giỏ hàng
- `addToCart(data)` - Thêm vào giỏ
- `updateCartItem(itemId, quantity)` - Cập nhật số lượng
- `removeFromCart(itemId)` - Xóa item
- `clearCart(customerId)` - Xóa toàn bộ

### Authentication (auth.js)

`AuthManager` class handle:
- JWT token storage (localStorage)
- Customer info persistence
- Login/logout
- Auth state checking

### UI Helpers

- `showToast(message, type)` - Toast notifications
- `showLoading(element)` - Loading states
- `updateCartBadge()` - Cart item count
- `formatCurrency(amount)` - Format tiền tệ
- `formatDate(dateString)` - Format ngày tháng

---

## 🚀 How to Run

### Step 1: Start Backend Services

```bash
cd customer_service
python manage.py runserver 8001

cd ../book_service
python manage.py runserver 8002

cd ../cart_service
python manage.py runserver 8003
```

### Step 2: Start Frontend Server

```bash
cd frontend
python server.py
```

### Step 3: Open Browser

Navigate to: **http://localhost:8000**

### Or Use Run Script

```bash
run_all.bat
```

Sẽ tự động khởi động cả 4 servers!

---

## 📱 User Flows

### Flow 1: Browse Books (Guest)

1. Mở `http://localhost:8000`
2. Xem danh sách sách
3. Tìm kiếm hoặc filter theo category
4. Click vào sách để xem details (via book card)

### Flow 2: Register & Login

1. Click "Register" trên nav
2. Điền form đăng ký
3. Submit → Redirect to login
4. Đăng nhập với credentials
5. Nhận JWT token → Redirect to home
6. Nav hiển thị username

### Flow 3: Add to Cart

1. Đăng nhập (required)
2. Browse books
3. Click "Add to Cart"
4. Toast notification xác nhận
5. Cart badge update với số lượng

### Flow 4: Manage Cart

1. Click "Cart" trên nav
2. Xem cart items với book details
3. Adjust quantity với +/- buttons
4. Remove items
5. See real-time total updates
6. Clear cart hoặc proceed to checkout

---

## 🎯 Key Features

### ✅ Inter-Service Communication

Cart hiển thị **full book details** từ Book Service:
- Title, author, category
- Current price
- Stock status
- Book image

### ✅ Real-time Updates

- Cart badge updates khi add/remove items
- Total price recalculates instantly
- Stock validation khi add to cart

### ✅ Error Handling

- Network errors → Toast notifications
- Service unavailable → Friendly error messages
- Invalid input → Form validation errors
- Auth required → Redirect to login

### ✅ Loading States

- Skeleton loaders khi fetch data
- Button loading states during submit
- Smooth transitions

### ✅ Responsive Design

**Breakpoints**:
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

**Adaptations**:
- Single column layout on mobile
- Collapsible navigation (future)
- Touch-friendly buttons
- Optimized grid columns

---

## 📸 UI Screenshots

### Color Scheme

![Design System](file:///C:/Users/Admin/.gemini/antigravity/brain/ce50f4d3-9ee2-4f35-977e-cf0542315d04/uploaded_image_1768878238408.png)

- Dark background (#0f172a)
- Vibrant accents (indigo, pink, green)
- Glassmorphism cards
- Animated gradients

---

## 🔧 Customization

### Change Color Scheme

Edit `style.css`:

```css
:root {
    --primary: #your-color;
    --secondary: #your-color;
    --accent: #your-color;
}
```

### Add New Pages

1. Create `newpage.html`
2. Include CSS và JS scripts
3. Use same header/nav structure
4. Add navigation link

### Extend API

Add methods to `api.js`:

```javascript
async customEndpoint(data) {
    return this.request(`${this.API_URL}/custom/`, {
        method: 'POST',
        body: JSON.stringify(data)
    });
}
```

---

## 🎨 Design Highlights

### Glassmorphism Cards

```css
.glass-card {
    background: rgba(30, 41, 59, 0.6);
    backdrop-filter: blur(10px);
    border-radius: 1rem;
    border: 1px solid rgba(148, 163, 184, 0.1);
}
```

### Animated Background

Radial gradients với infinite float animation

### Gradient Buttons

```css
.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### Hover Effects

- `translateY(-4px)` on cards
- Shadow elevation
- Color transitions
- Scale transforms

---

## 📝 Future Enhancements

Có thể thêm:

- [ ] Book detail modal
- [ ] Wishlist functionality
- [ ] Order history page
- [ ] User profile page
- [ ] Payment integration
- [ ] Dark/Light theme toggle
- [ ] Advanced search filters
- [ ] Pagination for books
- [ ] Lazy loading images
- [ ] Service worker (PWA)

---

## 🎉 Summary

**Created**:
- ✅ 4 HTML pages (Home, Login, Register, Cart)
- ✅ Complete CSS design system (600+ lines)
- ✅ 4 JavaScript modules (API, Auth, Books, Cart)
- ✅ Python frontend server với CORS
- ✅ Full API integration với 3 microservices
- ✅ Responsive, modern, professional design
- ✅ Dark theme với glassmorphism
- ✅ Smooth animations và transitions

**Total**: 9 frontend files

Hệ thống đã có **UI hoàn chỉnh và chuyên nghiệp**! 🚀
