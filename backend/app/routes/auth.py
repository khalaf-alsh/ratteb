from fastapi import APIRouter, Depends

from app.dependencies.auth import get_authenticated_user


router = APIRouter(
    prefix="/api",
    tags=["Auth"],
)


@router.get("/me")
def get_current_user(
    auth=Depends(get_authenticated_user),
):
    _, user = auth

    return {
        "id": user.id,
        "email": user.email,
    }