from shop_list.core.config import settings as s
from sqlalchemy.ext.asyncio import create_async_engine

connection_string = f"{s.POSTGRES_SCHEME}://{s.POSTGRES_USER}:{s.POSTGRES_PASSWORD}@{s.POSTGRES_SERVER}:{s.POSTGRES_PORT}/{s.POSTGRES_DB}"
engine = create_async_engine(connection_string)
