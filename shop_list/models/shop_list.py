from sqlalchemy import Column, String

from shop_list.db.base_class import SqlAlchemyBaseModel


class ShopList(SqlAlchemyBaseModel):
    __tablename__ = "shop_list"

    place: str = Column(String, nullable=True)
