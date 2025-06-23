from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload
from starlette.responses import JSONResponse

from app.base.logic import BaseLogic
from app.modules.listings.models import Listing, ListingAttachment
from app.modules.listings.schemas import ListingCreate, ListingUpdate
from app.modules.users.models import User
from app.modules.listings.schemas import ListingGet



class ListingBusinessLogic(BaseLogic):
    Model = Listing

    async def create(self, listing: ListingCreate, current_user: User):
        data = listing.model_dump(exclude={"attachment_ids"})
        data["created_by"] = current_user.id
        data = self.Model(**data)
        self.repository.session.add(data)

        for attachment_id in listing.attachment_ids:
            link = ListingAttachment(
                listing=data,
                attachment_id=attachment_id
            )
            self.repository.session.add(link)

        return listing

    async def get_all(self):
        stmt = (
            select(self.Model)
            .where(self.Model.deleted_at.is_(None), self.Model.deleted_by.is_(None))
            .options(joinedload(self.Model.attachments), joinedload(self.Model.creator))
            .order_by(self.Model.created_at.desc())
            )
        result = await self.repository.session.execute(stmt)
        listings = result.unique().scalars().all()
        return listings

    async def delete(self, id_: UUID, current_user: User):
        try:
            stmt = (
                update(self.Model).where(self.Model.id == id_)
                .values(
                    deleted_at=datetime.now(),
                    deleted_by=current_user.id
                )
            )
            result = await self.repository.session.execute(stmt)
            await self.repository.session.commit()

            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Listing not found")

            return JSONResponse(content={"detail": "Success"}, status_code=200)

        except NoResultFound:
            raise HTTPException(status_code=404, detail="Listing not found")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update(self, id_: UUID, listing: ListingUpdate, current_user: User):
        try:
            stmt = (
                update(self.Model)
                .where(self.Model.id == id_)
                .values(
                    title=listing.title,
                    description=listing.description,
                    price=listing.price,
                    property_type=listing.property_type,
                    updated_at=datetime.now(),
                    updated_by=current_user.id,
                )
            )
            await self.repository.session.execute(stmt)
            await self.repository.session.commit()

            stmt_select = (
                select(self.Model)
                .where(self.Model.id == id_)
                .options(joinedload(self.Model.attachments), joinedload(self.Model.creator))
            )
            result_select = await self.repository.session.execute(stmt_select)
            updated_listing = result_select.unique().scalar_one_or_none()

            if updated_listing is None:
                raise HTTPException(status_code=404, detail="Listing not found")

            # Фикс: возвращаем Pydantic-схему
            return ListingGet.model_validate(updated_listing)

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
