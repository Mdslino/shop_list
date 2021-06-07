from typing import Optional

from pydantic import UUID4, BaseModel


class ItemsBase(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None


class ItemsCreate(ItemsBase):
    name: str
    price: float


class ItemsUpdate(ItemsCreate):
    pass


class ItemsInDBBase(ItemsBase):
    id: Optional[UUID4]

    class Config:
        orm_mode = True


class ItemsInDB(ItemsInDBBase):
    pass


class Items(ItemsInDBBase):
    pass
