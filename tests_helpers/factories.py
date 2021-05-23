from uuid import uuid4

from factory import Sequence, lazy_attribute
from factory.alchemy import SQLAlchemyModelFactory
from shop_list.core import security
from shop_list.models import User

from tests_helpers import common


class UserFactory(SQLAlchemyModelFactory):
    id = Sequence(lambda n: uuid4())
    first_name = "Marcelo"
    last_name = "Lino"
    email = "mdslino@gmail.com"

    @lazy_attribute
    def hashed_password(self):
        return security.get_password_hash("password")

    class Meta:
        model = User
        sqlalchemy_session = common.Session
        sqlalchemy_session_persistence = "commit"
