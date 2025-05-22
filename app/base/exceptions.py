from fastapi import HTTPException


class InvalidFilterFieldError(HTTPException):
    """Ошибка: попытка фильтрации по несуществующему полю."""

    def __init__(self, field: str):
        super().__init__(
            status_code=400,
            detail=f"Фильтрация по полю '{field}' запрещена или оно не существует.",
        )
