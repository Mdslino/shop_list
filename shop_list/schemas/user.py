from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, validator


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

    @validator("verify_password")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords do not match")
        return v


class UserUpdate(UserBase):
    password: Optional[str]
    verify_password: Optional[str]

    @validator("verify_password")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["verify_password"]:
            raise ValueError("passwords do not match")
        return v


class UserInDBBase(UserBase):
    id: Optional[UUID4]

    class Config:
        orm_mode = True


class UserInDB(UserInDBBase):
    hashed_password: str


class User(UserInDBBase):
    pass
