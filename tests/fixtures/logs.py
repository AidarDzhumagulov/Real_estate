from datetime import datetime

import pytest

from app.modules.logs.models import Logs
from tests.utils import build_instances_core_api


@pytest.fixture()
async def logs_fixture(async_testing_session, documents_records, rooms_fixture, users_fixture):
    documents_ids = [doc[0] for doc in documents_records]
    logs_data = [
        {
            "type": "test_type_1",
            "name": "test_name_1",
            "description": "test_description_1",
            "document_id": documents_ids[0],
            "room_id": rooms_fixture[0][0],
            "user_id": users_fixture[0][0],
            "created_at": datetime(year=2021, month=1, day=1, hour=1, minute=1, second=1),
            "details": {"test_detail": "my_detail"},
        },
        {
            "type": "test_type_2",
            "name": "test_name_2",
            "description": "test_description_2",
            "document_id": documents_ids[1],
            "room_id": rooms_fixture[0][0],
            "user_id": users_fixture[0][0],
            "created_at": datetime(year=2021, month=1, day=1, hour=1, minute=1, second=2),
            "details": {"test_detail": "my_detail"},
        },
        {
            "type": "test_type_2",
            "name": "test_name_2",
            "description": "test_description_2",
            "document_id": documents_ids[1],
            "room_id": rooms_fixture[0][0],
            "user_id": users_fixture[0][0],
            "created_at": datetime(year=2021, month=1, day=1, hour=1, minute=1, second=3),
            "details": {"test_detail": "my_detail"},
        },
    ]

    async for item in build_instances_core_api(async_testing_session, Logs, logs_data):
        yield item
