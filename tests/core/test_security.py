from datetime import timedelta

import pytest
from faker import Faker
from shop_list.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)


@pytest.mark.parametrize(
    "password", [Faker().pystr(min_chars=1, max_chars=20) for x in range(10)]
)
def test_password_hash(password: str):
    hash = get_password_hash(password)
    assert hash != password
    assert len(hash) > len(password)
    assert verify_password(password, hash)


@pytest.mark.parametrize(
    "subject,delta", [(1, timedelta(minutes=15)), (2, None)]
)
def test_create_access_token(subject: int, delta: timedelta):
    token = create_access_token(subject, delta)
    assert isinstance(token, str)
    assert token
