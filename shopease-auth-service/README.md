# ShopEase Authentication Microservice

Independent authentication microservice using FastAPI, MySQL 8, SQLAlchemy, Alembic, bcrypt, JWT and Docker Compose.

## Features

- User registration with email validation
- Secure bcrypt password hashing
- User login and JWT access tokens
- Token expiration and signature validation
- Current authenticated user endpoint
- Token verification endpoint
- Authenticated password change
- Separate MySQL database and persistent Docker volume
- Alembic database migration

## Project structure

- `app/main.py` - FastAPI application
- `app/routers` - Authentication routes
- `app/models` - SQLAlchemy user model
- `app/schemas` - Pydantic request and response schemas
- `app/services` - Registration and login business logic
- `app/core` - Configuration and JWT/password security
- `app/database` - Database engine and session dependency
- `alembic` - Database migrations

## Environment

Configure `.env` with database credentials and a strong JWT secret.

## Start with Docker Compose

    docker compose up --build -d

The authentication API runs on port 8002.
MySQL is an independent container with persistent volume storage.

Swagger UI:

    http://localhost:8002/docs

## Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth/register` | Register a user |
| POST | `/api/auth/login` | Login and receive JWT |
| GET | `/api/auth/me` | Get current user |
| POST | `/api/auth/verify-token` | Verify JWT |
| POST | `/api/auth/change-password` | Change password |

## JWT usage

For protected endpoints, send:

    Authorization: Bearer YOUR_ACCESS_TOKEN

## Alembic

Create a migration:

    alembic revision --autogenerate -m "describe change"

Apply migrations:

    alembic upgrade head

Rollback one migration:

    alembic downgrade -1

## Security notes

- Passwords are stored as bcrypt hashes.
- JWT secrets and database credentials are configured through environment variables.
- `.env` must not be committed to GitHub.
- The default role for new users is `customer`.
- Access tokens expire according to `ACCESS_TOKEN_EXPIRE_MINUTES`.

## API testing

Use Swagger UI or Postman to test registration, login, token validation, current-user access and password changes. Record actual test results before submission.
