import datetime
import os
from urllib.parse import quote
from uuid import uuid4

import aiofiles
from fastapi import UploadFile, HTTPException
from sqlalchemy import select
from starlette import status
from starlette.responses import StreamingResponse

from app.base.logic import BaseLogic
from app.config import settings
from app.modules.attachments.models import Attachment
from app.modules.users.models import User


class AttachmentBusinessLogic(BaseLogic):
    Model = Attachment

    async def create(self,file: UploadFile,  current_user: User):
        _hash = f"{uuid4().hex}_{file.filename}"
        filename = file.filename
        os.makedirs(settings.TMP_STORAGE_PATH, exist_ok=True)
        file_path = os.path.join(settings.TMP_STORAGE_PATH, filename)

        async with aiofiles.open(file_path, "wb") as buffer:
            content = await file.read()
            await buffer.write(content)

        attachment = Attachment(
            mimetype=file.content_type,
            size=len(content),
            filename=filename,
            filepath=f"{settings.TMP_STORAGE_PATH}/{filename}",
            hash=_hash,
            created_at=datetime.datetime.now(),
            created_by=current_user.id,
        )
        self.repository.session.add(attachment)
        await self.repository.session.commit()
        await self.repository.session.refresh(attachment)
        return attachment

    async def get(self, id_: str):
        stmt = select(Attachment).where(Attachment.id == id_)
        result = await self.repository.session.execute(stmt)
        attachment = result.scalar_one_or_none()
        if not attachment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Attachment with hash '{hash}' not found"
            )
        try:
            file = await aiofiles.open(attachment.filepath, mode="rb")
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Файл не найден на сервере")
        return StreamingResponse(
            file,
            media_type=attachment.mimetype,
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{quote(attachment.filename)}"
            },
        )
