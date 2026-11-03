from datetime import datetime, timezone
from uuid import UUID, uuid4
from app.models.product_model import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate

class ProductService:
    # Temporary in-memory storage. Data resets when the application restarts.
    products: dict[str, Product] = {}

    @classmethod
    def create_product(cls, data: ProductCreate):
        product = Product(
            product_id=str(uuid4()),
            name=data.name,
            description=data.description,
            price=data.price,
            stock_quantity=data.stock_quantity,
            category=data.category,
            status=data.status.value,
            created_date=datetime.now(timezone.utc)
        )
        cls.products[product.product_id] = product
        return product

    @classmethod
    def get_products(cls, category=None, skip=0, limit=10):
        products = list(cls.products.values())

        if category:
            products = [
                product for product in products
                if product.category.lower() == category.lower()
            ]

        return products[skip:skip + limit]

    @classmethod
    def get_product(cls, product_id: UUID):
        return cls.products.get(str(product_id))

    @classmethod
    def update_product(cls, product_id: UUID, data: ProductUpdate):
        product = cls.products.get(str(product_id))
        if not product:
            return None

        product.name = data.name
        product.description = data.description
        product.price = data.price
        product.stock_quantity = data.stock_quantity
        product.category = data.category
        product.status = data.status.value

        return product

    @classmethod
    def delete_product(cls, product_id: UUID):
        return cls.products.pop(str(product_id), None) is not None
