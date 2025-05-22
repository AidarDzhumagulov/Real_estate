import pytest
from sqlalchemy import select

from app.modules.organizations.models import Organization


@pytest.mark.asyncio
async def test_update_by_organization_id(
    override_dependency,
    async_http_client,
    async_testing_session,
    mock_database_session,
    mock_database_session_in_middlewares,
    organizations_fixture,
    users_fixture,
    mock_jwt_token,
):
    headers = mock_jwt_token
    org_id = organizations_fixture[0][0]
    update_data = {"name": "Update Organization", "description": "Update description"}
    response = await async_http_client.put(
        f"/api/organizations/?organization_id={org_id}", json=update_data, headers=headers
    )
    result = response.json()
    assert result.get("message") == "Organization edited"
    organization_queryset = select(Organization).where(Organization.id == org_id)
    organization_queryset_result = await async_testing_session.scalar(organization_queryset)
    assert organization_queryset_result.name == update_data.get("name")
    assert organization_queryset_result.description == update_data.get("description")
