from enum import Enum
from typing import Dict, List, Type

from pydantic import BaseModel
from sqlalchemy import Column, Select, asc, desc

from app.database.session import Base


class SortDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"


class SortOption(BaseModel):
    field: str
    direction: SortDirection = SortDirection.DESC


class BaseSort:
    """
    Базовый класс для сортировки по существующим полям в таблице.
    Смотрите пример использования в api/notifications/v2/
    """

    Model: Type[Base]

    @classmethod
    def get_field_mapping(cls) -> Dict[str, Column]:
        """
        Автоматически создает маппинг полей модели в SQLAlchemy.

        :return: Колонка в виде строки и значение сама колонка.
        """
        assert cls.Model is not None, "Необходимо определить Model в наследниках BaseFilter"
        return {column.name: column for column in cls.Model.__table__.c}

    def _apply_sorting(self, query: Select, sort_options: List[SortOption]) -> Select:
        """
        Применяет сортировку к запросу.

        :param query: Исходный SQL-запрос.
        :param sort_options: Параметры сортировки.
        :return: Модифицированный SQL-запрос.
        """
        if not sort_options:
            return query

        field_mapping = self.get_field_mapping()

        sort_expressions = []
        for sort_option in sort_options:
            if sort_option.field in field_mapping:
                column = field_mapping[sort_option.field]
                if sort_option.direction == SortDirection.ASC:
                    sort_expressions.append(asc(column))
                else:
                    sort_expressions.append(desc(column))

        if sort_expressions:
            return query.order_by(*sort_expressions)

        # Если сортировка не задана, сортируем по `created_at`, если оно есть, иначе по первичному ключу
        default_sort_field = getattr(self.Model, "created_at", None) or next(
            iter(field_mapping.values())
        )
        return query.order_by(desc(default_sort_field))
