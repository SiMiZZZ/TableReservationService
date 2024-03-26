import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from config import settings
from datetime import datetime, timedelta

from schemas.user import UserData


def encode_jwt(payload: dict,
               private_key: str = settings.PRIVATE_KEY_PATH.read_text(),
               algorithm: str = settings.JWT_ALGORITHM,
               expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    to_encode = payload.copy()
    now = datetime.now()
    expire = now + timedelta(minutes=int(expire_minutes))
    to_encode.update(exp=expire, iat=now)
    encoded_jwt = jwt.encode(payload, private_key, algorithm=algorithm)
    return encoded_jwt

def decode_jwt(token: str,
               key: str = settings.PUBLIC_KEY_PATH.read_text(),
               algorithm: str = settings.JWT_ALGORITHM):
    decoded_jwt = jwt.decode(token, key, algorithms=[algorithm])
    return decoded_jwt


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    bytes_password: bytes = password.encode()
    return bcrypt.hashpw(bytes_password, salt)

def validate_password(password: str, hashed_password: bytes) -> bool:

    return bcrypt.checkpw(password.encode(), hashed_password)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
)

def get_current_token_payload(
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    token: str = Depends(oauth2_scheme),
) -> dict:
    # token = credentials.credentials
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
            # detail=f"invalid token error",
        )
    return payload
