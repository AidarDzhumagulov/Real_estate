from fastapi.testclient import TestClient
from sqlalchemy import delete, insert

from main import app

client = TestClient(app)


async def build_instances_core_api(session, model, instances_data):
    stmt = insert(model).returning(model.id).values(instances_data)
    created_instances_ids = await session.execute(stmt)
    ids = created_instances_ids.all()
    await session.commit()
    yield ids
    stmt = delete(model).where(model.id.in_([id_[0] for id_ in ids]))
    await session.execute(stmt)
    await session.commit()
