from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base
from app.utils.database.crud import MixinCRUD


class Listing(Base, MixinCRUD):
    __tablename__ = "listings"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column()
    property_type: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()
    city: Mapped[str] = mapped_column()

    attachments: Mapped[list["Attachment"]] = relationship(
        "Attachment",
        secondary="listings_attachments",
        back_populates="listings"
    )


class ListingAttachment(Base, MixinCRUD):
    __tablename__ = "listings_attachments"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    listing_id: Mapped[UUID] = mapped_column(ForeignKey("listings.id"), nullable=False)
    attachment_id: Mapped[UUID] = mapped_column(ForeignKey("attachments.id"), nullable=False)

    listing: Mapped["Listing"] = relationship("Listing", backref="listing_attachments")
    attachment: Mapped["Attachment"] = relationship("Attachment", backref="attachment_listings")


