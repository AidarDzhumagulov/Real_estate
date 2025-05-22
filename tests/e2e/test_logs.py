import pytest
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.modules.logs.models import Logs


@pytest.mark.asyncio
async def test_logs_by_document_id_view(
    override_dependency,
    async_http_client,
    async_testing_session,
    mock_database_session,
    mock_database_session_in_middlewares,
    mock_jwt_token,
    documents_records,
    logs_fixture,
    rooms_fixture,
):
    log = select(Logs).where(Logs.id == logs_fixture[0][0]).options(joinedload(Logs.user))
    log = await async_testing_session.execute(log)
    log = log.scalar()
    response = await async_http_client.get(
        f"/api/logs/document/?document_id={documents_records[0][0]}", headers=mock_jwt_token
    )
    jsonified_response = response.json()
    assert response.status_code == 200
    assert jsonified_response[0].get("type") == log.type
    assert jsonified_response[0].get("name") == log.name
