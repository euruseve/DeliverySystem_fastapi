from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status

from app.config import sec_settings


def generate_access_token(data: dict, expiry: timedelta = timedelta(seconds=15)) -> str:
    return jwt.encode(
        payload={
            **data,
            "exp": datetime.now(timezone.utc) + expiry,
        },
        algorithm=sec_settings.JWT_ALGORITHM,
        key=sec_settings.JWT_SECRET,
    )


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            jwt=token,
            key=sec_settings.JWT_SECRET,
            algorithms=[sec_settings.JWT_ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token"
        )
    except jwt.PyJWTError:
        return None
