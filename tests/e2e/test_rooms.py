import pytest

from app.modules.rooms.models import Room


@pytest.mark.asyncio
async def test_update_room(
    override_dependency,
    async_http_client,
    async_testing_session,
    mock_database_session,
    mock_database_session_in_middlewares,
    rooms_fixture,
    users_fixture,
    mock_jwt_token,
):
    room_id = rooms_fixture[0][0]
    json_body = {"name": "Update name", "custom_url": "http://209.38.238.41/athena/"}
    response = await async_http_client.put(
        f"/api/rooms/?id={room_id}",
        data=json_body,
        headers=mock_jwt_token,
    )
    assert response.status_code == 200

    room_obj = await async_testing_session.get(Room, room_id)
    assert room_obj.name == json_body.get("name")
    assert room_obj.custom_url == json_body.get("custom_url")
