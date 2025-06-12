from fastapi import APIRouter, Depends, Response

from app.middlewares.request_processing import RequestProcessingRoute
from app.modules.users.logic import (
    UserBusinessLogic,
)
from app.modules.users.schemas import AuthCredentials, UserBase
from app.utils.dependencies import get_current_user
from app.utils.jwt_utils import auth

user_router = APIRouter(
    tags=["Users"],
    prefix="/api/users",
    route_class=RequestProcessingRoute,
)


@user_router.post("/register/")
async def register_user(
    user: UserBase,
    user_logic: UserBusinessLogic = Depends(UserBusinessLogic.from_request),
):
    return await user_logic.create(user=user)


@user_router.post("/login/")
async def login(
    credentials: AuthCredentials,
    response: Response,
    user_logic: UserBusinessLogic = Depends(UserBusinessLogic.from_request),
):
    return await user_logic.login_user(credentials=credentials, response=response)


@user_router.get("/", dependencies=[Depends(auth.access_token_required)])
async def get_user(
    user_logic: UserBusinessLogic = Depends(UserBusinessLogic.from_request),
    current_user=Depends(get_current_user)
):
    return current_user

# #
# # @user_router.post("/login/verify/", response_model=schemas.Token)
# # async def verify_login(
# #     email: str = Form(),
# #     auth_password: str = Form(),
# #     browser_data: Optional[str] = Form(None),
# #     session: AsyncSession = Depends(get_session),
# # ):
# #     email = email.strip().lower()
# #     user = await session.scalar(select(User).where(User.email == email))
# #     user_auth = await session.scalar(
# #         select(UserAuth).where(
# #             and_(
# #                 UserAuth.user_id == user.id,
# #                 UserAuth.auth_password == auth_password,
# #             )
# #         )
# #     )
# #     if not user_auth:
# #         return DefaultResponse(
# #             success=False,
# #             status_code=400,
# #             message="False OTP",
# #         )
# #
# #     fingerprint = await logic.create_user_fingerprint_logic(
# #         browser_data=browser_data,
# #         session=session,
# #         user_id=user.id,
# #     )
# #     access_token = await logic.create_access_token(user, fingerprint.id if fingerprint else None)
# #     refresh_token = await logic.create_refresh_token(
# #         user, is_mobile=user_auth.is_mobile, fingerprint_id=fingerprint.id if fingerprint else None
# #     )
# #
# #     await session.execute(delete(UserAuth).where(UserAuth.id == user_auth.id))
# #     return {"access_token": access_token, "refresh_token": refresh_token}
#
#
# @user_router.post("/refresh-token/")
# async def refresh_token(
#     refresh_token_data: RefreshTokenSchema,
#     session: AsyncSession = Depends(get_session),
#     # TODO(protasov): Transition to fingerprint data during the sign-in process.
#     x_is_mobile: Optional[str] = Header(default=None),
# ):
#     token = refresh_token_data.refresh_token
#     is_blacklisted = await jwt_utils.is_token_blacklisted(session, token)
#     if is_blacklisted:
#         return DefaultResponse(success=False, message="Token blacklisted", status_code=401)
#     try:
#         new_access_token, new_refresh_token = jwt_utils.refresh_access_token(
#             token, is_mobile=x_is_mobile is not None
#         )
#     except TokenExpiredError:
#         return DefaultResponse(success=False, message="Token expired", status_code=401)
#     except InvalidTokenError:
#         return DefaultResponse(success=False, message="Invalid token", status_code=401)
#     except IsNotRefreshTokenError:
#         return DefaultResponse(success=False, message="Not a refresh token", status_code=401)
#     return {"access_token": new_access_token, "refresh_token": new_refresh_token}
#
#
# @user_router.post("/logout/")
# async def logout(
#     request: Request,
#     session: AsyncSession = Depends(get_session),
# ):
#     auth = request.headers["Authorization"]
#     _, token = auth.split()
#     await TokenBlacklist.add_tokens_to_blacklist(
#         session=session,
#         access_token=token,
#     )
#     return DefaultResponse(success=True, message="Successfully logged out")
#
# #
# # @user_router.post("/send-restore/")
# # async def send_restore_password_email_view(
# #     email_data: schemas.EmailRestorePassword,
# #     session: AsyncSession = Depends(get_session),
# #     queue_connector: "KafkaConnector" = Depends(get_kafka_connector),
# # ):
# #     user = await User.get_user_by_email(session, email_data.email)
# #     if user is None:
# #         raise HTTPException(
# #             status_code=404,
# #             detail={"status": False, "message": "User not found"},
# #         )
# #     # We mustn't clear password in this place.
# #     # temp_password = "".join(random.choices(string.ascii_letters + string.digits, k=12))
# #     # hashed_temp_password = Hasher.get_password_hash(temp_password)
# #     await User.update_attributes_by_conditions(
# #         session,
# #         {"id": user.id},
# #         {
# #             # "hashed_password": hashed_temp_password,
# #             "previous_password": user.hashed_password,
# #         },
# #     )
# #     await logic.send_restore_password_email_logic(
# #         session=session, email=email_data.email, user=user, kafka_connector=queue_connector
# #     )
# #     ws_data = {
# #         "message": "User was disconnected",
# #         "event": "disconnect_user",
# #         "details": {"user_id": str(user.id)},
# #         "is_personal": True,
# #     }
# #     await queue_connector.send_message(message=ws_data, topic_name=settings.KAFKA_SESSION_TOPIC)
# #     return DefaultResponse(success=True, message="Email was sent")
# #
# #
# # @user_router.post("/restore/")
# # async def restore_password_view(
# #     restore_data: schemas.RestorePassword,
# #     session: AsyncSession = Depends(get_session),
# #     log_context: dict = Depends(get_log_context),
# #     queue_connector: "KafkaConnector" = Depends(get_kafka_connector),
# # ):
# #     link_instance = await session.scalar(
# #         select(UserEmailLink).where(UserEmailLink.id == restore_data.link_id)
# #     )
# #     if link_instance.used_at is not None:
# #         raise HTTPException(
# #             status_code=400,
# #             detail={"status": False, "message": "Link already used"},
# #         )
# #     user = (await session.execute(select(User).where(User.id == restore_data.user_id))).scalar()
# #     if not user:
# #         raise HTTPException(
# #             status_code=404,
# #             detail={"status": False, "message": "User not found"},
# #         )
# #     if Hasher.verify_password(restore_data.password, user.hashed_password) or (
# #         user.previous_password
# #         and Hasher.verify_password(restore_data.password, user.previous_password)
# #     ):
# #         raise HTTPException(
# #             status_code=400,
# #             detail={
# #                 "status": False,
# #                 "message": "New password cannot be the same as the old password",
# #             },
# #         )
# #     await logic.restore_password_logic(
# #         session=session,
# #         restore_data=restore_data,
# #     )
# #     ws_data = {
# #         "type": "system",
# #         "method": "close_all_users_connections",
# #         "params": {"user_id": str(user.id)},
# #     }
# #     await queue_connector.send_message(message=ws_data, topic_name=settings.KAFKA_SESSION_TOPIC)
# #     log_context.update({"action_code": "RESTORE_PASSWORD", "account": user.id})
# #     return DefaultResponse(success=True, message="Password restored")
#
#
# @user_router.put("/phone_lang/")
# async def set_phone_language(
#     lang: PhoneLanguage,
#     session: AsyncSession = Depends(get_session),
# ):
#     await logic.set_phone_language(session, lang.fbtoken, lang.language)
#     return DefaultResponse(success=True, status_code=200)
#
#
# @user_router.post("/change_pincode/")
# async def change_pincode_view(
#     pincode_data: schemas.PincodeSchema,
#     session: AsyncSession = Depends(get_session),
#     current_user: User = Depends(get_current_user),
# ):
#     await logic.change_pincode_logic(
#         session=session,
#         pincode_data=pincode_data,
#         current_user=current_user,
#     )
#     return DefaultResponse(success=True, message="Pincode create or changed successfully")
#
#
# @user_router.post("/verif_pincode/")
# async def verify_pincode_view(
#     pincode_data: schemas.PincodeSchema,
#     current_user: User = Depends(get_current_user),
# ):
#     result = await logic.verif_pincode_logic(
#         pincode_data=pincode_data,
#         current_user=current_user,
#     )
#     return result
#
#
# @user_router.get("/global/")
# async def get_global_user_by_room_and_organization_view(
#     session: AsyncSession = Depends(get_session),
#     current_user: User = Depends(get_current_user),
# ):
#     result = await logic.get_global_user_by_room_and_organization_logic(
#         session=session,
#         current_user=current_user,
#     )
#     return result
#
#
# @user_router.put("/auth/")
# async def update_user_auth_type(
#     tfa_enabled: bool,
#     session: AsyncSession = Depends(get_session),
#     current_user: User = Depends(get_current_user),
# ):
#     await session.execute(
#         update(User).where(User.id == current_user.id).values(tfa_enabled=tfa_enabled)
#     )
#     return DefaultResponse(
#         success=True,
#         status_code=200,
#         message="User auth type was successfully updated",
#     )
#
#
# # @user_router.post("/send_code/")
# # async def send_code(
# #     current_user: User = Depends(get_current_user),
# #     user_logic: UserBusinessLogic = Depends(UserBusinessLogic.from_request),
# #     queue_connector: "KafkaConnector" = Depends(get_kafka_connector),
# # ):
# #     await user_logic.send_code(current_user, queue_connector)
# #     return DefaultResponse(
# #         success=True,
# #         status_code=200,
# #         message="Code successfully sent",
# #     )
#
#
# @user_router.post("/pincode_verification/")
# async def code_verification(
#     pincode: schemas.PincodeSchema,
#     current_user: User = Depends(get_current_user),
#     user_logic: UserBusinessLogic = Depends(UserBusinessLogic.from_request),
# ):
#     await user_logic.verify_pincode(pincode.pincode, current_user)
#     return DefaultResponse(
#         success=True,
#         status_code=200,
#         message="Code was correct",
#     )
#
#
# @user_router.post("/link/validate/", response_model=UserEmailLinkValidateSchema)
# async def validate_email_link(
#     link_id: uuid.UUID,
#     user_logic: UserBusinessLogic = Depends(UserBusinessLogic.from_request),
# ):
#     result = await user_logic.validate_email_link(link_id=link_id)
#     return UserEmailLinkValidateSchema.model_validate(result)
#
#
# @user_router.post("/fingerprint/refresh/")
# async def refresh_fingerprint_tokens(
#     browser_data: str = Form(None),
#     x_is_mobile: Optional[bool] = Header(default=False),
#     current_user: User = Depends(get_current_user),
#     user_logic: UserBusinessLogic = Depends(UserBusinessLogic.from_request),
#     log_context: dict = Depends(get_log_context),
# ):
#     return await user_logic.refresh_user_fingerprint_and_tokens(
#         browser_data=browser_data,
#         current_user=current_user,
#         is_mobile=x_is_mobile,
#         log_context=log_context,
#     )
#
#
# @user_router.get("/v2/")
# async def get_users(
#     user_filter: Annotated[BaseFilterSchema, Depends(BaseFilterSchema.from_query)],
#     user_logic: UserBusinessLogic = Depends(UserBusinessLogic.from_request),
# ):
#     return await user_logic.get(filter_params=user_filter)
