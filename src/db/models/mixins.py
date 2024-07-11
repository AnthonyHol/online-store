import uuid
from datetime import datetime

from sqlalchemy import DateTime, func, String
from sqlalchemy.orm import Mapped, mapped_column


class GUIDMixin:
    """Mixin of implement id."""

    __abstract__ = True

    guid: Mapped[str] = mapped_column(
        String(255), primary_key=True, default=lambda: str(uuid.uuid4())
    )


class CreatedAtMixin:
    """Mixin to implement created_at field."""

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class UpdatedAtMixin:
    """Mixin to implement updated_at field."""

    __abstract__ = True

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
