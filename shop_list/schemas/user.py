from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr


class UserBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    first_name: str
    last_name: str
    email: str
    password: str
    verify_password: str


class UserUpdate(UserBase):
    password: Optional[str]
    verify_password: Optional[str]


class UserInDBBase(UserBase):
    id: Optional[UUID4]

    class Config:
        orm_mode = True


class UserInDB(UserInDBBase):
    hashed_password: str


class User(UserInDBBase):
    pass
