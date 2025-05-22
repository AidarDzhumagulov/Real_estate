from typing import List, Optional, Type

from fastapi import Depends
from sqlalchemy import ColumnElement

from app.base.repositories import BaseRepository
from app.database.session import Base


class BaseLogic:
    """
    You need add base service model
    to work with Built-in methods such as "isntance_by_id".

    ________________________________

    For example:

        class SomeLogic:
            Model = SomeModel

    ________________________________
    """

    Model = None

    def __init__(self, repository: BaseRepository = None):
        self.repository = repository

    def __init_subclass__(cls, **kwargs):
        if cls.Model is None:
            raise NotImplementedError(
                f"{cls.__name__} doesn't implement Model class. \n\n"  # noqa: EM102
                f"See documentation app/base/logic.py."
            )

    @classmethod
    def from_request(
        cls,
        repository: BaseRepository = Depends(BaseRepository.from_request),
    ):
        return cls(repository=repository)

    def isntance_by_id(
        self,
        instance_id,
        additional_filters: Optional[List[ColumnElement[bool]]] = None,
        model: Optional[Type[Base]] = None,
    ):
        if not model:
            model = self.Model

        return self.repository.get_by_id(
            Model=model,
            instance_id=instance_id,
            additional_filters=additional_filters,
        )
