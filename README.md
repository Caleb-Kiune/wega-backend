# WEGA Kitchenware Backend API Specification

## 1. Project Overview

### Tech Stack
- **Framework**: Flask (Python)
- **Database**: SQLite (Development) → PostgreSQL (Production)
- **ORM**: SQLAlchemy
- **Authentication**: JWT + HTTP-only cookies
- **Documentation**: Swagger/OpenAPI

### Environment Setup
```bash
# .env.example
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=sqlite:///dev.db
POSTGRES_URL=postgresql://user:pass@localhost:5432/wega
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
```

## 2. Mock Data Inventory

### Products
```json
{
  "id": 1,
  "name": "Premium Non-Stick Frying Pan",
  "price": 2499,
  "image": "/images/kitchenware1.jpeg",
  "category": "Cookware",
  "description": "High-quality non-stick frying pan",
  "stock": 50,
  "isNew": true,
  "isSale": false,
  "createdAt": "2024-03-15T10:00:00Z",
  "updatedAt": "2024-03-15T10:00:00Z"
}
```

### Categories
```json
[
  {
    "id": 1,
    "name": "Cookware",
    "slug": "cookware",
    "description": "High-quality cooking equipment"
  }
]
```

### Locations
```json
{
  "id": "nairobi-cbd",
  "name": "Nairobi CBD",
  "shippingPrice": 250,
  "isActive": true
}
```

## 3. API Endpoints & Schemas

### Authentication

#### POST /api/auth/register
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```
Response (201):
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user",
  "createdAt": "2024-03-15T10:00:00Z"
}
```

#### POST /api/auth/login
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```
Response (200):
```json
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refreshToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user"
  }
}
```

#### POST /api/auth/refresh
Response (200):
```json
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Products

#### GET /api/products
Query Parameters:
- `page`: number (default: 1)
- `limit`: number (default: 20)
- `category`: string
- `search`: string
- `sort`: string (price_asc, price_desc, newest)
- `minPrice`: number
- `maxPrice`: number

Response (200):
```json
{
  "data": [
    {
      "id": 1,
      "name": "Premium Non-Stick Frying Pan",
      "price": 2499,
      "image": "/images/kitchenware1.jpeg",
      "category": "Cookware",
      "description": "High-quality non-stick frying pan",
      "stock": 50,
      "isNew": true,
      "isSale": false,
      "createdAt": "2024-03-15T10:00:00Z",
      "updatedAt": "2024-03-15T10:00:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

### Cart

#### GET /api/cart
Response (200):
```json
{
  "items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "Premium Non-Stick Frying Pan",
        "price": 2499,
        "image": "/images/kitchenware1.jpeg"
      },
      "quantity": 2
    }
  ],
  "subtotal": 4998,
  "shipping": 250,
  "total": 5248
}
```

### Orders

#### POST /api/orders
```json
{
  "shippingAddress": {
    "location": "nairobi-cbd",
    "details": "123 Main St"
  },
  "paymentMethod": "mpesa",
  "promoCode": "WELCOME10"
}
```
Response (201):
```json
{
  "id": 1,
  "status": "pending",
  "shippingAddress": "Nairobi CBD, 123 Main St",
  "shippingPrice": 250,
  "subtotal": 4998,
  "discount": 499.8,
  "total": 4748.2,
  "paymentMethod": "mpesa",
  "paymentStatus": "pending",
  "items": [
    {
      "product": {
        "id": 1,
        "name": "Premium Non-Stick Frying Pan",
        "price": 2499,
        "image": "/images/kitchenware1.jpeg"
      },
      "quantity": 2,
      "price": 2499
    }
  ],
  "createdAt": "2024-03-15T10:00:00Z"
}
```

## 4. Error Handling

### Standard Error Response
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "email": ["Invalid email format"],
      "password": ["Password must be at least 8 characters"]
    }
  }
}
```

### HTTP Status Codes
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 422: Validation Error
- 429: Too Many Requests
- 500: Internal Server Error

## 5. Database Schema

### Entity Relationship Diagram
```
[Users] 1--* [Orders]
[Users] 1--* [CartItems]
[Users] 1--* [WishlistItems]
[Products] 1--* [CartItems]
[Products] 1--* [OrderItems]
[Products] 1--* [WishlistItems]
[Categories] 1--* [Products]
[Orders] 1--* [OrderItems]
[PromoCodes] 1--* [Orders]
```

### Tables
```sql
-- Enable foreign keys
PRAGMA foreign_keys = ON;

-- Users
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  name TEXT NOT NULL,
  role TEXT DEFAULT 'user',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Categories
CREATE TABLE categories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  description TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Products
CREATE TABLE products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT,
  price REAL NOT NULL,
  category_id INTEGER REFERENCES categories(id),
  stock INTEGER NOT NULL,
  image TEXT,
  is_new BOOLEAN DEFAULT FALSE,
  is_sale BOOLEAN DEFAULT FALSE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Cart Items
CREATE TABLE cart_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER REFERENCES users(id),
  product_id INTEGER REFERENCES products(id),
  quantity INTEGER NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Orders
CREATE TABLE orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER REFERENCES users(id),
  status TEXT NOT NULL,
  shipping_address TEXT NOT NULL,
  shipping_price REAL NOT NULL,
  subtotal REAL NOT NULL,
  discount REAL DEFAULT 0,
  total REAL NOT NULL,
  payment_method TEXT NOT NULL,
  payment_status TEXT NOT NULL,
  promo_code_id INTEGER REFERENCES promo_codes(id),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Order Items
CREATE TABLE order_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER REFERENCES orders(id),
  product_id INTEGER REFERENCES products(id),
  quantity INTEGER NOT NULL,
  price REAL NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Wishlist Items
CREATE TABLE wishlist_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER REFERENCES users(id),
  product_id INTEGER REFERENCES products(id),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Promo Codes
CREATE TABLE promo_codes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  code TEXT UNIQUE NOT NULL,
  discount_percent INTEGER NOT NULL,
  expiry_date DATETIME NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_cart_items_user ON cart_items(user_id);
CREATE INDEX idx_wishlist_items_user ON wishlist_items(user_id);
CREATE INDEX idx_promo_codes_code ON promo_codes(code);
```

## 6. Middleware Stack

1. **CORS Middleware**
   ```python
   CORS(app, resources={
       r"/api/*": {
           "origins": ["https://wega-kitchenware.vercel.app"],
           "methods": ["GET", "POST", "PUT", "DELETE"],
           "allow_headers": ["Content-Type", "Authorization"]
       }
   })
   ```

2. **JWT Authentication**
   - Verify access token in Authorization header
   - Refresh token in HTTP-only cookie
   - Rate limit: 100 requests per minute

3. **Input Validation**
   - Request body validation using Marshmallow
   - Query parameter validation
   - File upload validation

4. **Logging**
   - Request/response logging
   - Error logging
   - Performance metrics

5. **Rate Limiting**
   - Global: 1000 requests per hour
   - Auth endpoints: 5 requests per minute
   - Admin endpoints: 100 requests per hour

## 7. Security Measures

1. **Input Validation**
   - Sanitize all user inputs
   - Validate file uploads
   - Prevent SQL injection

2. **Authentication**
   - JWT with short expiration (15 minutes)
   - HTTP-only refresh tokens
   - Rate limiting on auth endpoints

3. **Authorization**
   - Role-based access control
   - Resource ownership validation
   - Admin-only routes protection

4. **Data Protection**
   - Password hashing with bcrypt
   - Sensitive data encryption
   - Secure session management

5. **API Security**
   - CORS policy
   - Rate limiting
   - Request size limits
   - XSS/CSRF protection

## 8. Development Setup

1. **Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Database**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

3. **API Documentation**
   ```bash
   flask swagger
   ```

4. **Testing**
   ```bash
   pytest
   ```

## 9. Production Deployment

1. **Database Migration**
   ```bash
   # Update DATABASE_URL in .env
   flask db upgrade
   ```

2. **Environment Variables**
   - Set production secrets
   - Configure CORS origins
   - Set up logging

3. **Security**
   - Enable HTTPS
   - Set secure cookies
   - Configure rate limits

## 10. Optional Enhancements

1. **Image Upload**
   - Cloud storage integration
   - Image optimization
   - CDN delivery

2. **Notifications**
   - Email notifications
   - SMS notifications
   - Push notifications

3. **Analytics**
   - Order tracking
   - Sales analytics
   - User behavior tracking

4. **Internationalization**
   - Multi-language support
   - Currency conversion
   - Regional pricing

5. **Performance**
   - Caching layer
   - Database optimization
   - API response compression 