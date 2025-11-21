
from datetime import datetime, timedelta
from typing import Any, Union
import bcrypt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app import models

ALGORITHM = "HS256"
MAX_BCRYPT_LENGTH = 72

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

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
    return bcrypt.checkpw(
        truncate_password(plain_password).encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(
        truncate_password(password).encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> models.User:
    """Decode JWT Bearer token and return the authenticated user.

    Raises 401 if the token is missing/invalid or the user no longer exists.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == sub).first()
    if user is None:
        raise credentials_exception
    return user

