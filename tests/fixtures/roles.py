import pytest

from app.modules.roles.models import Role
from tests.utils import build_instances_core_api


@pytest.fixture
async def roles_fixture(async_testing_session):
    roles_data = [
        {
            "name": "my_role_name",
            "permissions": ["permission_1", "permission_2"],
        },
        {
            "name": "my_role_name_2",
            "permissions": ["permission_2", "permission_3"],
        },
        {
            "name": "full_administrator",
            "permissions": ["permission_2", "permission_3"],
        },
        {
            "name": "restricted_administrator",
            "permissions": ["permission_2", "permission_3"],
        },
        {
            "name": "service_administrator",
            "permissions": ["permission_2", "permission_3"],
        },
        {
            "name": "user",
            "permissions": ["permission_2", "permission_3"],
        },
    ]
    async for item in build_instances_core_api(async_testing_session, Role, roles_data):
        yield item
