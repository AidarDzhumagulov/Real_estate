import enum
import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import FetchedValue, Enum
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import (
    Mapped,
    mapped_column, relationship,
)
from sqlalchemy.sql.functions import concat

from app.database.session import Base
from app.utils.database.crud import MixinCRUD

if TYPE_CHECKING:
    from app.modules.listings.models import Listing


class UserRole(enum.Enum):
    AGENT = "agent"
    CLIENT = "client"
    ADMIN = "admin"


class User(Base, MixinCRUD):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        server_default=FetchedValue(),
    )
    first_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()
    previous_password: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(nullable=True)
    user_avatar_url: Mapped[Optional[str]] = mapped_column(nullable=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.CLIENT)

    listings: Mapped[list["Listing"]] = relationship(back_populates="creator", foreign_keys="Listing.created_by")

    @property
    def is_authenticated(self) -> bool:
        return True

    @hybrid_property
    def user_name(self) -> str:  # type: ignore
        # First and last name can be None
        if self.first_name is None and self.last_name is None:
            return self.email
        return " ".join(filter(None, [self.first_name, self.last_name]))

    @user_name.setter
    def user_name(self, value):
        self.user_name = value

    @user_name.expression
    @classmethod
    def user_name(cls):
        return concat(cls.first_name, " ", cls.last_name)
