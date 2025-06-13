from fastapi import APIRouter, Depends, UploadFile, File
from starlette.responses import StreamingResponse

from app.middlewares.request_processing import RequestProcessingRoute
from app.modules.attachments.logic import AttachmentBusinessLogic
from app.utils.jwt_utils import auth
from app.utils.dependencies import get_current_user

attachment_router = APIRouter(
    tags=["Attachments"],
    prefix="/api/attachments",
    route_class=RequestProcessingRoute,
)


@attachment_router.post("/", dependencies=[Depends(auth.access_token_required)])
async def upload(
    file: UploadFile = File(...),
    attachment_logic: AttachmentBusinessLogic = Depends(AttachmentBusinessLogic.from_request),
    current_user=Depends(get_current_user)
):
    return await attachment_logic.create(file=file, current_user=current_user)


@attachment_router.get(f"/")
async def download(id_: str, attachment_logic: AttachmentBusinessLogic = Depends(AttachmentBusinessLogic.from_request)) -> StreamingResponse:
    return await attachment_logic.get(id_)
