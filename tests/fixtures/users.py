from datetime import datetime

import pytest
from jose import jwt

from app.config import settings
from app.modules.user_sessions.models import Session
from app.modules.users.models import User, UserFingerprint
from tests.utils import build_instances_core_api


@pytest.fixture
async def users_fixture(async_testing_session):
    # user password is my_test_password
    user_data = [
        {
            "email": "testemail@test.tet",
            "first_name": "myfirstname",
            "last_name": "mylastname",
            "phone_number": "+88005553535",
            "hashed_password": "$2a$04$pKzxyvQ/aLCT1VGTNr0hYOPCfDge/AC1bXvA5HQQXTDR535Y3l51i",
            "user_avatar_url": "localhost:5555",
        },
        {
            "email": "another@test.tet",
            "first_name": "myfirstname2",
            "last_name": "mylastname",
            "phone_number": "+88005553535",
            "hashed_password": "$2a$04$pKzxyvQ/aLCT1VGTNr0hYOPCfDge/AC1bXvA5HQQXTDR535Y3l51i",
            "user_avatar_url": "localhost:5555",
        },
    ]

    async for item in build_instances_core_api(async_testing_session, User, user_data):
        yield item


@pytest.fixture
async def user_fingerprint_fixture(async_testing_session, users_fixture):
    users_ids = [u[0] for u in users_fixture]
    user_data = [
        {
            "user_id": users_ids[0],
            "fingerprint_data": {
                "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "accept": "accept-ranges: bytes",
            },
        },
    ]

    async for item in build_instances_core_api(async_testing_session, UserFingerprint, user_data):
        yield item


@pytest.fixture
async def user_session_fixture(async_testing_session, users_fixture, user_fingerprint_fixture):
    users_ids = [u[0] for u in users_fixture]
    user_fingerprints = [u[0] for u in user_fingerprint_fixture]
    user_data = [
        {
            "user_id": users_ids[0],
            "fingerprint_id": user_fingerprints[0],
            "ip": "127.0.0.2",
            "location": "Valhalla",
            "start_at": datetime.now(),
        },
    ]

    async for item in build_instances_core_api(async_testing_session, Session, user_data):
        yield item


@pytest.fixture
async def relate_users_vs_rooms(async_testing_session, rooms_fixture, users_fixture):
    users_ids = [u[0] for u in users_fixture]
    rooms_ids = [r[0] for r in rooms_fixture]

    for user_id in users_ids:
        await User.add_user_to_room(async_testing_session, user_id, rooms_ids[0])
    return rooms_ids[0]


@pytest.fixture(scope="session")
async def mock_jwt_token():
    to_encode = {"sub": "testemail@test.tet"}

    token = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return {"authorization": f"Bearer {token}"}
