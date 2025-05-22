import json
from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel

from app.base.filters import FilterCondition
from app.base.sorts import SortOption


class PaginationInfo(BaseModel):
    pages: int
    current: int
    per_page: int
    total: int


class BaseFilterSchema(BaseModel):
    filters: Optional[List["FilterCondition"]] = None
    sort: Optional[List["SortOption"]] = None

    @classmethod
    def from_query(
        cls,
        filters: Optional[str] = Query(None, description="JSON-строка с фильтрами"),
        sort: Optional[str] = Query(None, description="JSON-строка с сортировкой"),
    ) -> "BaseFilterSchema":
        """
        Парсит JSON-строку с фильтрами и сортировкой из query params.
        """
        try:
            filters_parsed = json.loads(filters) if filters else None
            sort_parsed = json.loads(sort) if sort else None
        except json.JSONDecodeError:
            raise ValueError("Неверный формат JSON в параметрах запроса")  # noqa: EM101

        return cls(
            filters=[FilterCondition(**f) for f in filters_parsed] if filters_parsed else None,
            sort=[SortOption(**s) for s in sort_parsed] if sort_parsed else None,
        )
