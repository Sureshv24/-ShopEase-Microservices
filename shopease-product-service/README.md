# ShopEase Product Service

A Product Microservice built using FastAPI, Python, Pydantic and Docker.

## Features

- Create products
- Retrieve all products
- Filter products by category
- Pagination using skip and limit
- Retrieve a product by ID
- Update products
- Delete products
- Input validation
- In-memory data storage
- Docker support

## Run locally

Install dependencies:

    pip install -r requirements.txt

Start the application:

    uvicorn app.main:app --reload --port 8003

Swagger documentation:

    http://localhost:8003/docs

## Docker

Build:

    docker build -t shopease-product-service .

Run:

    docker run -d --name shopease-product-container -p 8003:8003 shopease-product-service

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/products/ | Create product |
| GET | /api/products/ | List products |
| GET | /api/products/{product_id} | Get product |
| PUT | /api/products/{product_id} | Update product |
| DELETE | /api/products/{product_id} | Delete product |

## Storage

This assignment uses in-memory storage. Product data is not permanently saved and resets when the application restarts.
