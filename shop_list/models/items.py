from decimal import Decimal
from uuid import UUID as UUIDType

from sqlalchemy import (
    DECIMAL,
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from shop_list.db.base_class import SqlAlchemyBaseModel
from shop_list.models.shop_list import ShopList


class Items(SqlAlchemyBaseModel):
    __tablename__ = "items"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_quantity_positive"),
    )

    shop_list_id: UUIDType = Column(
        UUID(as_uuid=True), ForeignKey("shop_list.id"), nullable=False
    )
    name: str = Column(String, nullable=False)
    price: Decimal = Column(DECIMAL(10, 2), nullable=False)
    quantity: int = Column(Integer, nullable=False)

    shop_list: ShopList = relationship("ShopList", uselist=False)
