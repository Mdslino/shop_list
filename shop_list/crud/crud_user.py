from typing import Any, Dict, Optional, Union

from shop_list.core.security import get_password_hash, verify_password
from shop_list.models.user import User
from shop_list.schemas.user import UserCreate, UserUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(
        self, db: AsyncSession, *, email: str
    ) -> Optional[User]:
        statement = select(self.model).where(self.model.email == email)
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        db_obj = self.model(
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
        )

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]],
    ) -> User:
        if isinstance(obj_in, dict):
            updated_data = obj_in
        else:
            updated_data = obj_in.dict(exclude_unset=True)

        if password := updated_data.get("password"):
            hashed_password = get_password_hash(password)
            updated_data["password"] = hashed_password

        return await super().update(db, db_obj=db_obj, obj_in=updated_data)

    async def authenticate(
        self, db: AsyncSession, *, email: str, password: str
    ) -> Optional[User]:
        if user := await self.get_by_email(db, email=email):
            if verify_password(password, user.hashed_password):
                return user
        return None


user = CRUDUser(User)
