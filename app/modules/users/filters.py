from uuid import UUID

from sqlalchemy import Select, and_, any_
from sqlalchemy.orm import aliased

from app.base.filters import BaseFilter
from app.modules.users.models import User


class UserFilter(BaseFilter):
    Model = User
