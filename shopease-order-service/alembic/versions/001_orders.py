from alembic import op
import sqlalchemy as sa
revision="001_orders"; down_revision=None; branch_labels=None; depends_on=None
def upgrade():
    op.create_table("orders",
      sa.Column("id",sa.Integer(),primary_key=True),sa.Column("order_number",sa.String(40),nullable=False,unique=True),
      sa.Column("user_id",sa.Integer(),nullable=False),sa.Column("shipping_address",sa.JSON(),nullable=False),
      sa.Column("subtotal",sa.Numeric(12,2),nullable=False),sa.Column("discount_amount",sa.Numeric(12,2),nullable=False,server_default="0.00"),
      sa.Column("shipping_charge",sa.Numeric(12,2),nullable=False),sa.Column("tax_amount",sa.Numeric(12,2),nullable=False),
      sa.Column("total_amount",sa.Numeric(12,2),nullable=False),sa.Column("order_status",sa.String(20),nullable=False,server_default="PENDING"),
      sa.Column("payment_status",sa.String(20),nullable=False,server_default="PENDING"),sa.Column("notes",sa.Text()),
      sa.Column("cancellation_key",sa.String(80),unique=True),sa.Column("created_at",sa.DateTime(),nullable=False),
      sa.Column("updated_at",sa.DateTime(),nullable=False))
    op.create_index("ix_orders_user_id","orders",["user_id"]); op.create_index("ix_orders_order_status","orders",["order_status"])
    op.create_table("order_items",sa.Column("id",sa.Integer(),primary_key=True),
      sa.Column("order_id",sa.Integer(),sa.ForeignKey("orders.id",ondelete="CASCADE"),nullable=False),
      sa.Column("product_id",sa.Integer(),nullable=False),sa.Column("product_name",sa.String(180),nullable=False),
      sa.Column("sku",sa.String(80),nullable=False),sa.Column("unit_price",sa.Numeric(12,2),nullable=False),
      sa.Column("quantity",sa.Integer(),nullable=False),sa.Column("discount_amount",sa.Numeric(12,2),nullable=False,server_default="0.00"),
      sa.Column("total_price",sa.Numeric(12,2),nullable=False),sa.Column("created_at",sa.DateTime(),nullable=False))
    op.create_index("ix_order_items_order_id","order_items",["order_id"]); op.create_index("ix_order_items_product_id","order_items",["product_id"])
def downgrade():
    op.drop_table("order_items"); op.drop_table("orders")
