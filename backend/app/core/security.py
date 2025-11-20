
from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# Configure bcrypt so that it never raises on >72-byte passwords.
# We perform explicit truncation ourselves in truncate_password, but this
# ensures other call sites using this context also behave safely in CI.
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__truncate_error=False,
)

ALGORITHM = "HS256"
MAX_BCRYPT_LENGTH = 72

def truncate_password(password: str) -> str:
    # Truncate to 72 bytes (not characters—may need encoding if non-ASCII)
    encoded = password.encode('utf-8')
    return encoded[:MAX_BCRYPT_LENGTH].decode('utf-8', 'ignore')

def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(truncate_password(plain_password), hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(truncate_password(password))
