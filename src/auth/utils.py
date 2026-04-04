from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Response
from src.core.config import auth_settings

auth_data = auth_settings.get_auth_data


def create_token(data: dict, expire_timedelta: timedelta, token_type: str):
    to_encode = data.copy()
    if "sub" in to_encode and not isinstance(to_encode["sub"], str):
        to_encode["sub"] = str(to_encode["sub"])
    expire = datetime.now(timezone.utc) + expire_timedelta
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(
        to_encode,
        key=auth_data[f"{token_type}_secret_key"],
        algorithm=auth_data["algorithm"],
    )


def generate_tokens(data: dict, response: Response):
    access_token = create_token(data, timedelta(minutes=15), "access")
    refresh_token = create_token(data, timedelta(days=7), "refresh")
    tokens = [
        ("access_token", access_token),
        ("refresh_token", refresh_token),
    ]
    for key, value in tokens:
        response.set_cookie(key=key, value=value, httponly=True, samesite="lax")
    return {"access_token": access_token, "refresh_token": refresh_token}
