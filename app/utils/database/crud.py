from datetime import datetime
from typing import Optional

from sqlalchemy import UUID, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column


class MixinCRUD:
    """
    Добавляет общие поля для всех таблиц

    created_at: Дата создания сущности
    created_by: Инициатор создания сущности
    updated_at: Дата обновления сущности
    updated_by: Инициатор обновления сущности
    deleted_at: Дата удаления сущности
    deleted_by: Инициатор удаления сущности
    """

    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, default=datetime.utcnow
    )

    @declared_attr
    def created_by(self):
        return mapped_column(UUID, ForeignKey("users.id"), nullable=True)

    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, onupdate=datetime.utcnow
    )

    @declared_attr
    def updated_by(self):
        return mapped_column(UUID, ForeignKey("users.id"), nullable=True)

    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    @declared_attr
    def deleted_by(self):
        return mapped_column(UUID, ForeignKey("users.id"), nullable=True)
