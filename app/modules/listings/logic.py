from sqlalchemy import select

from app.base.logic import BaseLogic
from app.modules.listings.models import Listing
from app.modules.listings.schemas import ListingCreate
from app.modules.users.models import User


class ListingBusinessLogic(BaseLogic):
    Model = Listing

    async def create(self, listing: ListingCreate, current_user: User):
        listing = listing.model_dump()
        listing["created_by"] = current_user.id
        self.repository.session.add(self.Model(**listing))

        return listing

    async def get_all(self):
        stmt = select(self.Model)
        result = await self.repository.session.execute(stmt)
        listings = result.scalars().all()
        return listings
