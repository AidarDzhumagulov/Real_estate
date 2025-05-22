import pytest
from sqlalchemy import delete

from app.modules.users.models import User


@pytest.mark.asyncio
async def test_login_user(
    override_dependency,
    async_http_client,
    users_fixture,
):
    json_body = {
        "email": "testemail@test.tet",
        "password": "my_test_password",
    }
    response = await async_http_client.post("api/users/login/", json=json_body)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_register_user(
    override_dependency,
    async_http_client,
    async_testing_session,
    roles_fixture,
    groups_fixture,
):
    json_body = {
        "email": "gpt@test.tet",
        "password": "my_test_password",
        "first_name": "Mikasa",
        "last_name": "Ackerman",
        "phone_number": "+88005553535",
        "invite_type": "master",
        "is_accepted_agreement": True,
    }
    response = await async_http_client.post("api/users/register/", json=json_body)
    assert response.status_code == 200
    assert response.json()["data"]["email"] == json_body["email"]
    await async_testing_session.execute(delete(User).where(User.email == json_body["email"]))


@pytest.mark.asyncio
async def test_register_user_returns_400(
    override_dependency,
    async_http_client,
    roles_fixture,
    groups_fixture,
):
    json_body = {
        "email": "gpt@test.tet",
        "password": "my_test_password",
        "first_name": "Mikasa",
        "last_name": "Ackerman",
        "phone_number": "+88005553535",
        "invite_type": "master",
    }
    response = await async_http_client.post("api/users/register/", json=json_body)
    assert response.status_code == 400
    assert response.json()["message"] == "Ошибка регистрации. Соглашение не принято"
