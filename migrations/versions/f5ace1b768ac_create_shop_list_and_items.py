"""CREATE_SHOP_LIST_AND_ITEMS

Revision ID: f5ace1b768ac
Revises: 530d6dc16381
Create Date: 2021-05-29 20:33:16.687330

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "f5ace1b768ac"
down_revision = "530d6dc16381"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "shop_list",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("place", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_shop_list_id"), "shop_list", ["id"], unique=True)
    op.create_table(
        "items",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column(
            "shop_list_id", postgresql.UUID(as_uuid=True), nullable=False
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("price", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.CheckConstraint("quantity > 0", name="check_quantity_positive"),
        sa.ForeignKeyConstraint(
            ["shop_list_id"],
            ["shop_list.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_items_id"), "items", ["id"], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_items_id"), table_name="items")
    op.drop_table("items")
    op.drop_index(op.f("ix_shop_list_id"), table_name="shop_list")
    op.drop_table("shop_list")
    # ### end Alembic commands ###