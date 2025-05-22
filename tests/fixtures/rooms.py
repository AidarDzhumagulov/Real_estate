from datetime import datetime

import pytest

# from app.modules.groups.models import UserGroupRoom
from app.modules.rooms.models import Room
from tests.utils import build_instances_core_api


@pytest.fixture
async def rooms_fixture(async_testing_session, users_fixture):
    rooms_data = [
        {
            "name": "test_room_1",
            "description": "test_room_1_description",
            "status": 1,
            "owner_id": users_fixture[0][0],
            "created_at": datetime(2022, 12, 12),
        },
        {
            "name": "test_room_2",
            "description": "test_room_1_description",
            "status": 2,
            "owner_id": users_fixture[0][0],
            "created_at": datetime(2022, 12, 12),
        },
    ]

    async for item in build_instances_core_api(async_testing_session, Room, rooms_data):
        yield item
