from datetime import datetime
from decimal import Decimal
from sqlalchemy import Integer, String, Text, DateTime, Numeric, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.connection import Base
class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_number: Mapped[str] = mapped_column(String(40), unique=True, nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    shipping_address: Mapped[dict] = mapped_column(JSON, nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12,2), nullable=False)
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(12,2), default=Decimal("0"), nullable=False)
    shipping_charge: Mapped[Decimal] = mapped_column(Numeric(12,2), nullable=False)
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12,2), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12,2), nullable=False)
    order_status: Mapped[str] = mapped_column(String(20), default="PENDING", nullable=False, index=True)
    payment_status: Mapped[str] = mapped_column(String(20), default="PENDING", nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)
    cancellation_key: Mapped[str | None] = mapped_column(String(80), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan", lazy="selectin")
