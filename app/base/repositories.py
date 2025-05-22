from typing import Coroutine, List, Optional

from fastapi import Depends
from sqlalchemy import ColumnElement, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.utils.dependencies import get_session


class BaseRepository:
    @classmethod
    async def from_request(cls, session: AsyncSession = Depends(get_session)):
        return cls(session)

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def execute(self, query) -> Coroutine:
        return self.session.execute(query)

    def scalar(self, query) -> Coroutine:
        return self.session.scalar(query)

    def scalars(self, query) -> Coroutine:
        return self.session.scalars(query)

    def get_by_id(
        self,
        Model,  # noqa: N803
        instance_id,
        additional_filters: Optional[List[ColumnElement[bool]]] = None,
    ):
        if not additional_filters:
            additional_filters = []
        return self.session.scalar(
            select(Model).where(
                *additional_filters,
                Model.id == instance_id,
            )
        )
