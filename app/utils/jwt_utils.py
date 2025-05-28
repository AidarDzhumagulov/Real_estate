from datetime import datetime, timedelta
from typing import Optional, Tuple

from authx import AuthXConfig, AuthX
from jose import ExpiredSignatureError, JWTError, jwt
from starlette.authentication import AuthenticationError

from app.config import settings


class CodeAuthenticationError(AuthenticationError):
    def __init__(self, message: str, code: int = 500):
        self.message = message
        self.code = code


class InvalidTokenError(JWTError):
    ...


class TokenExpiredError(ExpiredSignatureError):
    ...


class IsRefreshTokenError(JWTError):
    ...


class IsNotRefreshTokenError(JWTError):
    ...


def create_access_token(*, data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except ExpiredSignatureError as e:
        raise CodeAuthenticationError(str(e), code=401) from e
    except JWTError as e:
        raise InvalidTokenError from e


def decode_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if "is_refresh" not in payload:
            raise IsNotRefreshTokenError
        return payload
    except ExpiredSignatureError as e:
        raise TokenExpiredError from e
    except JWTError as e:
        raise InvalidTokenError from e


def create_refresh_token(
    *, data: dict, expires_delta: Optional[timedelta] = None, is_mobile: bool
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        delta = (
            settings.REFRESH_TOKEN_MOBILE_EXPIRE_MINUTES
            if is_mobile
            else settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
        expire = datetime.utcnow() + timedelta(minutes=delta)
    to_encode.update({"exp": expire})
    to_encode.update({"is_refresh": True})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def refresh_access_token(refresh_token: str, is_mobile: bool) -> Tuple[str, str]:
    payload = decode_refresh_token(refresh_token)
    new_payload = {"sub": payload.get("sub")}
    if fingerprint := payload.get("fingerprint_id"):
        new_payload["fingerprint_id"] = fingerprint
    new_access_token = create_access_token(data=new_payload)
    new_refresh_token = create_refresh_token(data=new_payload, is_mobile=is_mobile)
    return new_access_token, new_refresh_token


config = AuthXConfig(
     JWT_ALGORITHM=settings.JWT_ALGORITHM,
     JWT_SECRET_KEY=settings.SECRET_KEY,
     JWT_TOKEN_LOCATION=["cookies"],
     JWT_COOKIE_CSRF_PROTECT=False,
)

auth = AuthX(config=config)

