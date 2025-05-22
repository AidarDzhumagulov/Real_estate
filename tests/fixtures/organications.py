import pytest

from app.modules.organizations.models import Organization
from tests.utils import build_instances_core_api


@pytest.fixture
async def organizations_fixture(
    async_testing_session,
):
    organizations_data = [
        {
            "name": "my_organization_name",
        },
        {
            "name": "my_organization_name_2",
        },
        {
            "name": "my_organization_name_3",
        },
    ]

    async for item in build_instances_core_api(
        async_testing_session, Organization, organizations_data
    ):
        yield item
