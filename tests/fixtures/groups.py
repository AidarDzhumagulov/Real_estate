import pytest

from app.modules.groups.models import Group
from tests.utils import build_instances_core_api


@pytest.fixture
async def groups_fixture(
    async_testing_session,
):
    groups_data = [
        {
            "type": "test_group_1",
            "name": "my_group_name",
        },
        {
            "type": "test_group_2",
            "name": "my_group_name_2",
        },
        {
            "type": "test_group_3",
            "name": "my_group_name_3",
        },
    ]

    async for item in build_instances_core_api(async_testing_session, Group, groups_data):
        yield item
