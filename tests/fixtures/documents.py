from datetime import datetime

import pytest

from app.modules.documents.models import Document
from tests.utils import build_instances_core_api


@pytest.fixture
async def documents_records(async_testing_session):
    documents_data = [
        {
            "name": "test_document_1",
            "description": "test_document_1_description",
            "extension": "test_document_1_extension",
            "document_id": "test_document_1_id",
            "size": 1024,
            "created_at": datetime(2022, 12, 12),
            "author": "test_document_1_author",
            "modified_at": datetime(2022, 12, 12),
            "printed_at": datetime(2022, 12, 12),
            "version": 12,
            "token": "b569f8be-cb87-4072-b834-94822d225550",
            "hash": "test_document_1_hash",
            "upload_at": datetime(2022, 12, 12),
        },
        {
            "name": "test_document_2",
            "description": "test_document_2_description",
            "extension": "test_document_2_extension",
            "document_id": "test_document_2_id",
            "size": 1024,
            "created_at": datetime(2022, 12, 12),
            "author": "test_document_2_author",
            "modified_at": datetime(2022, 12, 12),
            "printed_at": datetime(2022, 12, 12),
            "version": 12,
            "token": "b569f8be-cb87-4072-b834-94822d225550",
            "hash": "test_document_2_hash",
            "upload_at": datetime(2022, 12, 12),
        },
    ]
    async for item in build_instances_core_api(async_testing_session, Document, documents_data):
        yield item
