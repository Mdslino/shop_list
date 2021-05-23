from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from shop_list import crud, models, schemas
from shop_list.api import deps
from shop_list.core import security
from shop_list.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
async def login_access_token(
    db: AsyncSession = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    if user := await crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    ):
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        return {
            "access_token": security.create_access_token(
                user.id, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )


@router.post("/login/test-token", response_model=schemas.User)
def test_token(
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Test access token
    """
    return current_user
