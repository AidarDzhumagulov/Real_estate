from fastapi import APIRouter, Depends

from app.middlewares.request_processing import RequestProcessingRoute
from app.modules.listings.logic import ListingBusinessLogic
from app.modules.listings.schemas import ListingCreate
from app.utils.jwt_utils import auth
from app.utils.dependencies import get_current_user

listing_router = APIRouter(
    tags=["Listings"],
    prefix="/api/listings",
    route_class=RequestProcessingRoute,
)


@listing_router.post("/", dependencies=[Depends(auth.access_token_required)])
async def create(
    listing: ListingCreate,
    listing_logic: ListingBusinessLogic = Depends(ListingBusinessLogic.from_request),
    current_user=Depends(get_current_user)
):
    return await listing_logic.create(listing=listing, current_user=current_user)


@listing_router.get("/", dependencies=[Depends(auth.access_token_required)])
async def get_all(listing_logic: ListingBusinessLogic = Depends(ListingBusinessLogic.from_request)):
    return await listing_logic.get_all()
