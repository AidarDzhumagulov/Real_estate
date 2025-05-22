from math import ceil
from typing import Dict, Generic, List, Tuple, TypeVar, Union

from sqlalchemy import func
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

int_or_str = TypeVar("int_or_str", int, str)
T = TypeVar("T")


class AsyncPaginator(Generic[T]):
    """
    Класс для асинхронной пагинации запросов SQLAlchemy.

    :param page: Номер страницы (по умолчанию 1).
    :param per_page: Количество элементов на странице (по умолчанию 20).
    :param count_via_distinct: Использовать DISTINCT при подсчете (по умолчанию True).
    """

    def __init__(
        self, page: int_or_str = 1, per_page: int_or_str = 20, count_via_distinct: bool = True
    ):
        self._count_via_distinct = count_via_distinct
        self._page = int(page) if page is not None else 1
        self._per_page = int(per_page) if per_page is not None else 20
        self._count = 0
        self._pages = 0

    @property
    def pagination_info(self) -> Dict[str, int]:
        """
        Возвращает информацию о текущем состоянии пагинации.

        :return: Словарь с мета-данными пагинации (количество страниц, текущая страница и т. д.).
        """
        return {
            "pages": self._pages,
            "current": self._page,
            "per_page": self._per_page,
            "total": self._count,
        }

    async def paginate_query(
        self, session: AsyncSession, query: Select, count_column=None
    ) -> Tuple[Result, Dict[str, int]]:
        """
        Выполняет пагинацию для переданного SQLAlchemy-запроса.

        :param session: Асинхронная сессия SQLAlchemy.
        :param query: SQL-запрос для получения данных.
        :param count_column: Колонка для подсчета записей (если None, используется func.count()).
        :return: Кортеж из результата запроса и информации о пагинации.
        """
        await self._calculate_count(session, query, count_column)

        # Если per_page отрицательный, возвращаем все записи
        if self._per_page < 0:
            self._page = 1
            self._per_page = self._count

        self._pages = ceil(self._count / self._per_page) if self._count else 1

        paginated_query = query.limit(self._per_page).offset((self._page - 1) * self._per_page)
        result = await session.execute(paginated_query)

        return result, self.pagination_info

    async def _calculate_count(
        self, session: AsyncSession, query: Select, count_column=None
    ) -> None:
        """
        Вычисляет общее количество записей в запросе.

        :param session: Асинхронная сессия SQLAlchemy.
        :param query: SQL-запрос для подсчета записей.
        :param count_column: Колонка для подсчета (если None, используется func.count()).
        """
        if count_column is None:
            count_expr = func.count()
        else:
            count_expr = func.count(
                count_column.distinct() if self._count_via_distinct else count_column
            )

        count_query = query.with_only_columns(count_expr).order_by(None)

        result = await session.execute(count_query)
        self._count = result.scalar() or 0


class PaginatedResponse(Generic[T]):
    """
    Объект, содержащий результаты пагинации.

    :param items: Список элементов текущей страницы.
    :param pagination: Данные о пагинации.
    """

    def __init__(self, items: List[T], pagination: Dict[str, int]):
        self.items = items
        self.pagination = pagination

    def dict(self) -> Dict[str, Union[List[T], Dict[str, int]]]:
        """
        Преобразует объект в словарь.

        :return: Словарь с элементами и мета-данными пагинации.
        """
        return {"data": self.items, "pagination": self.pagination}


async def paginate_query(
    session: AsyncSession, query: Select, page: int = 1, per_page: int = 20, count_column=None
) -> PaginatedResponse:
    """
    Вспомогательная функция для выполнения пагинации запроса.

    :param session: Асинхронная сессия SQLAlchemy.
    :param query: SQL-запрос, который нужно пагинировать.
    :param page: Номер страницы (по умолчанию 1).
    :param per_page: Количество записей на странице (по умолчанию 20).
    :param count_column: Колонка для подсчета записей (если None, используется func.count()).
    :return: Объект PaginatedResponse с результатами.
    """
    paginator = AsyncPaginator(page=page, per_page=per_page)
    result, pagination_info = await paginator.paginate_query(session, query, count_column)

    return PaginatedResponse(items=result.all(), pagination=pagination_info)
