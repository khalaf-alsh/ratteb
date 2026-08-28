from fastapi import Header, HTTPException

from app.supabase_client import supabase


def get_authenticated_user(
    authorization: str | None = Header(default=None),
):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header is missing",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header",
        )

    access_token = authorization.removeprefix("Bearer ").strip()

    try:
        response = supabase.auth.get_user(access_token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )

    user = response.user

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return access_token, user