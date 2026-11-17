# ShopEase Order Management Microservice

Independent FastAPI order service with a dedicated MySQL database.

## APIs
- POST `/api/orders/` create order
- GET `/api/orders/` list own orders; admins can list all; filters: page, page_size, status, date_from, date_to
- GET `/api/orders/{order_id}` retrieve order
- GET `/api/orders/number/{order_number}` retrieve by order number
- GET `/api/orders/{order_id}/items` retrieve item snapshots
- PATCH `/api/orders/{order_id}/status` administrator status update
- POST `/api/orders/{order_id}/cancel` cancel eligible order

## Integrations
JWT is verified using the shared Authentication Service signing secret and algorithm. User address lookup uses `GET /api/users/addresses/{address_id}`. Product endpoints used: `GET /api/products/{id}`, `POST /api/inventory/{id}/stock-out`, `POST /api/inventory/{id}/stock-in`. Confirm the User Service address route and response structure against the deployed API. Inventory write routes in the supplied Catalog implementation are administrator-protected; configure `INVENTORY_SERVICE_TOKEN` with a dedicated authorized service/admin JWT so stock operations do not use the customer token.

## Status transitions
PENDING -> CONFIRMED or CANCELLED; CONFIRMED -> PROCESSING or CANCELLED; PROCESSING -> SHIPPED or CANCELLED; SHIPPED -> DELIVERED. DELIVERED and CANCELLED are terminal.

## Pricing
Subtotal = regular product price x quantity. Discount uses Product Catalog `discount_price`. Tax defaults to 5% on discounted subtotal. Shipping defaults to 50 and is waived at discounted subtotal >= 1000. Total = subtotal - discount + tax + shipping. Calculations use Decimal.

## Inventory consistency
Stock is reserved through Product Catalog before local order persistence; a compensating stock-in is attempted if local persistence fails. Cancellation restores stock before marking the order cancelled. Cross-service operations are not atomic. Strict exactly-once stock restoration requires Product Catalog to persist and deduplicate the `Idempotency-Key` header; add this support to the Catalog service before relying on retry-safe compensation.

## Docker and migrations
`docker compose up --build -d`; Swagger: http://localhost:8006/docs.
Alembic: `alembic upgrade head`; `alembic revision --autogenerate -m "description"`; `alembic downgrade -1`.
Never commit `.env`.
