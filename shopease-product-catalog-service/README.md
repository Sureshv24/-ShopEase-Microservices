# ShopEase Product Catalog Microservice

Independent FastAPI service for product catalog, categories, search, filtering and inventory management.

## Stack
Python 3.11, FastAPI, Pydantic, SQLAlchemy, MySQL 8, Alembic, JWT and Docker Compose.

## Database
Dedicated database: `shopease_product_catalog_db`. Compose connects using hostname `catalog-db`. Tables: `categories`, `products`, `inventory_transactions`.

## JWT
This service validates JWT access tokens issued by the existing ShopEase Authentication Service. It uses the same signing secret and algorithm. It does not implement registration or login. Administrator routes require the JWT `role` claim to be `admin` or `administrator`. Customer-facing product and category reads expose active records only.

## APIs
### Products
- POST `/api/products/` (admin)
- GET `/api/products/` (active products; search, category_id, min_price, max_price, available, page, page_size, sort_by, sort_order)
- GET `/api/products/{product_id}` (active product)
- PUT/PATCH `/api/products/{product_id}` (admin)
- DELETE `/api/products/{product_id}` (admin)

### Categories
- POST `/api/categories/` (admin)
- GET `/api/categories/` (active categories)
- GET `/api/categories/{category_id}`
- PUT/DELETE `/api/categories/{category_id}` (admin)

A category containing products cannot be deleted. Reassign or delete its products first.

### Inventory
- GET `/api/inventory/{product_id}`
- POST `/api/inventory/{product_id}/stock-in` (admin)
- POST `/api/inventory/{product_id}/stock-out` (admin)
- GET `/api/inventory/{product_id}/history` (admin)
- GET `/api/inventory/low-stock?threshold=5` (admin)

Stock changes and history records are committed in one database transaction. Row locking is used to serialize stock changes on MySQL/InnoDB.

## Environment
Copy `.env.example` to `.env` and set unique database credentials and the same JWT secret/algorithm as Authentication Service. Never commit `.env`.

## Run with Docker
`docker compose up --build -d`

Swagger: http://localhost:8005/docs

Stop without deleting persistent data: `docker compose down`

## Alembic
`alembic upgrade head`
`alembic revision --autogenerate -m "describe change"`
`alembic downgrade -1`

## Local development
`python -m venv venv`
`.\venv\Scripts\Activate.ps1`
`pip install -r requirements.txt`
Set `DATABASE_URL` to a local MySQL connection and run `alembic upgrade head`, then `uvicorn app.main:app --reload --port 8005`.