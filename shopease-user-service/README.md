# ShopEase User Management Microservice

Independent FastAPI service for customer profiles and delivery addresses.

## Technology

- Python 3.11
- FastAPI and Pydantic
- MySQL 8 and SQLAlchemy
- Alembic migrations
- JWT validation
- Docker and Docker Compose

## Architecture

Authentication Service owns registration, login, passwords and JWT creation.
User Service validates the existing JWT and manages profile and address data.
The User Service does not store passwords or authentication credentials.

## APIs

### Profiles

- POST `/api/users/profile`
- GET `/api/users/profile`
- PUT `/api/users/profile`
- PATCH `/api/users/profile`
- DELETE `/api/users/profile`
- PATCH `/api/users/profile/deactivate`

### Addresses

- POST `/api/users/addresses`
- GET `/api/users/addresses`
- GET `/api/users/addresses/{address_id}`
- PUT `/api/users/addresses/{address_id}`
- PATCH `/api/users/addresses/{address_id}`
- DELETE `/api/users/addresses/{address_id}`
- PATCH `/api/users/addresses/{address_id}/default`

All profile and address endpoints require a Bearer JWT from the Authentication Service.

## Authentication integration

The User Service validates the JWT signature, expiration and `sub` claim using the same HS256 secret and algorithm configured in the Authentication Service. The JWT secret must be identical in both services and must be kept private.

The User Service never accepts an authentication user ID from the client as proof of ownership. It derives the ID from the verified JWT.

## Database

The separate database is `shopease_user_db`. The User Service connects to MySQL through the Compose hostname `user-db`.

The `user_profiles.auth_user_id` field is unique. Addresses belong to local profile IDs. Address queries are always scoped to the authenticated user's profile.

The profile `is_active` flag is local to this service. Deactivating a profile does not deactivate or delete the Authentication Service account. Coordinate account status changes with the Authentication Service separately.

## Environment

Configure `.env` with database credentials and the shared JWT settings. Never commit `.env`.

## Docker

    docker compose up --build -d

Swagger:

    http://localhost:8004/docs

Stop:

    docker compose down

The named MySQL volume persists when containers are stopped or removed. Do not use `docker compose down -v` unless you intend to delete the database volume.

## Alembic

    alembic upgrade head

Create a migration:

    alembic revision --autogenerate -m "describe change"

Rollback:

    alembic downgrade -1

## API testing

Swagger UI and Postman can be used with an access token obtained from the Authentication Service. Record actual results before reporting the service as fully tested.