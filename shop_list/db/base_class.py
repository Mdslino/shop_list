from datetime import datetime
from typing import Optional
from uuid import UUID as UUIDType
from uuid import uuid4

from sqlalchemy import Column, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SqlAlchemyBaseModel(Base):
    __abstract__ = True

    id: UUIDType = Column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
        primary_key=True,
        unique=True,
        default=uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    created_at: datetime = Column(
        DateTime, nullable=False, default=datetime.now
    )
    updated_at: Optional[datetime] = Column(
        DateTime, nullable=True, onupdate=datetime.now
    )
