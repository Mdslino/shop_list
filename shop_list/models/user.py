from shop_list.db.base_class import SqlAlchemyBaseModel
from sqlalchemy import String, Column


class User(SqlAlchemyBaseModel):
    __tablename__ = "users"

    first_name: str = Column(String, nullable=False)
    last_name: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False, index=True)
    hashed_password: str = Column(String, nullable=False)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
