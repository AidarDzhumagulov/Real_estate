from __future__ import annotations

from enum import Enum
from typing import Any, ClassVar, Dict, List, Tuple, Type, Union

from pydantic import BaseModel
from sqlalchemy import (
    JSON,
    Column,
    Integer,
    Select,
    String,
    Update,
    and_,
    cast,
)
from sqlalchemy.dialects.postgresql import JSONB

from app.base.exceptions import InvalidFilterFieldError
from app.database.session import Base


class FilterOperator(str, Enum):
    EQ = "eq"  # равно
    NE = "ne"  # не равно
    GT = "gt"  # больше
    GTE = "gte"  # больше или равно
    LT = "lt"  # меньше
    LTE = "lte"  # меньше или равно
    IN = "in"  # в списке
    NOT_IN = "not_in"  # не в списке
    ISNULL = "isnull"  # является NULL
    ILIKE = "ilike"  # через ilike


class FilterCondition(BaseModel):
    field: str
    value: Any


class BaseFilter:
    """
    Базовый класс для фильтрации по существующим полям в таблице.
    Смотрите пример использования в api/notifications/v2/
    """

    Model: Type[Base]

    CUSTOM_FILTERS: ClassVar = {}

    @classmethod
    def get_field_mapping(cls) -> Dict[str, Column]:
        """
        Автоматически создает маппинг полей модели в SQLAlchemy.
        """
        assert cls.Model is not None, "Необходимо определить Model в наследниках BaseFilter"
        return {column.name: column for column in cls.Model.__table__.c}

    @classmethod
    def get_json_fields(cls) -> Dict[str, Column]:
        """
        Выделяет JSON-поля модели.
        """
        return {
            column.name: column
            for column in cls.Model.__table__.c
            if isinstance(column.type, JSON)
        }

    def _apply_filters(
        self, query: Union[Select, Update], filters: List[FilterCondition]
    ) -> Union[Select, Update]:
        """Применяет фильтры к запросу."""
        if not filters:
            return query

        filter_conditions = []
        field_mapping = self.get_field_mapping()
        json_fields = self.get_json_fields()

        for filter_condition in filters:
            field, value = filter_condition.field, filter_condition.value
            op = self._infer_operator(value)

            custom_result = self._apply_custom_filter(query, filter_condition)
            if custom_result is not None:
                query, condition = custom_result
                filter_conditions.append(condition)
                continue

            if "." in field and field.split(".")[0] in json_fields:
                json_field_name, json_path = field.split(".", 1)
                column = json_fields[json_field_name]
                filter_expr = self._apply_json_filter(column, json_path, op, value)
            elif field in field_mapping:
                column = field_mapping[field]
                filter_expr = self._apply_filter_operator(column, op, value)
            else:
                raise InvalidFilterFieldError(field)

            if filter_expr is not None:
                filter_conditions.append(filter_expr)

        return query.where(and_(*filter_conditions)) if filter_conditions else query

    def _apply_json_filter(self, column, json_path: str, op: FilterOperator, value: Any):
        """Применяет фильтр к JSON-полю."""

        keys = json_path.split(".")

        json_expr = column
        for i, key in enumerate(keys):
            if isinstance(json_expr.type, (JSON, JSONB)):
                json_expr = json_expr[key]
                if i == len(keys) - 1:
                    json_expr = cast(json_expr, String)
            else:
                break

        if isinstance(value, str):
            json_expr = cast(json_expr, String)
        elif isinstance(value, int):
            json_expr = cast(json_expr, Integer)

        return self._apply_filter_operator(json_expr, op, value)

    @staticmethod
    def _infer_operator(value: Any) -> FilterOperator:
        """Автоматически определяет оператор фильтрации."""
        if isinstance(value, str):
            return FilterOperator.ILIKE
        if isinstance(value, list):
            return FilterOperator.IN
        if value is None:
            return FilterOperator.ISNULL
        return FilterOperator.EQ

    def _apply_custom_filter(
        self, query: Select, filter_: FilterCondition
    ) -> Tuple[Select, Any] | None:
        """Применяет кастомный фильтр и возвращает (новый query, условие) или None."""
        filter_func = self.CUSTOM_FILTERS.get(filter_.field)
        if filter_func:
            return filter_func(query, filter_.value)
        return None

    @staticmethod
    def _apply_filter_operator(column, op: FilterOperator, value: Any):
        """
        Применяет оператор фильтрации к колонке.

        :param column: Колонка для фильтрации.
        :param op: Оператор фильтрации.
        :param value: Значение для сравнения.
        :return: SQL-выражение для фильтрации.
        """
        if op == FilterOperator.EQ:
            return column == value
        elif op == FilterOperator.NE:
            return column != value
        elif op == FilterOperator.GT:
            return column > value
        elif op == FilterOperator.GTE:
            return column >= value
        elif op == FilterOperator.LT:
            return column < value
        elif op == FilterOperator.LTE:
            return column <= value
        elif op == FilterOperator.IN:
            return column.in_(value)
        elif op == FilterOperator.NOT_IN:
            return column.not_in(value)
        elif op == FilterOperator.ILIKE:
            return column.ilike(f"%{value}%")
        elif op == FilterOperator.ISNULL:
            return column.is_(None) if value else column.is_not(None)
        return None
