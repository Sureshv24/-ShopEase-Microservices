from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.security import get_authenticated_user_id
from app.schemas.user_schema import (
    UserProfileCreate, UserProfileUpdate, UserProfileResponse, MessageResponse
)
from app.services import user_service

router = APIRouter(prefix="/api/users", tags=["User Profiles"])

@router.post("/profile", response_model=UserProfileResponse, status_code=201)
def create_user_profile(
    data: UserProfileCreate,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    return user_service.create_profile(db, auth_user_id, data)

@router.get("/profile", response_model=UserProfileResponse)
def read_user_profile(
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    return user_service.get_profile(db, auth_user_id)

@router.put("/profile", response_model=UserProfileResponse)
def replace_user_profile(
    data: UserProfileCreate,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    return user_service.update_profile(db, auth_user_id, data.model_dump())

@router.patch("/profile", response_model=UserProfileResponse)
def partially_update_user_profile(
    data: UserProfileUpdate,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    return user_service.update_profile(
        db, auth_user_id, data.model_dump(exclude_unset=True)
    )

@router.delete("/profile", status_code=status.HTTP_204_NO_CONTENT)
def remove_user_profile(
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    user_service.delete_profile(db, auth_user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/profile/deactivate", response_model=MessageResponse)
def deactivate_user_profile(
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    user_service.deactivate_profile(db, auth_user_id)
    return {"message": "User profile deactivated. Authentication account is unchanged."}