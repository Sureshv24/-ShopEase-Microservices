from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.user_model import UserProfile
from app.schemas.user_schema import UserProfileCreate, UserProfileUpdate

def create_profile(db: Session, auth_user_id: int, data: UserProfileCreate):
    existing = db.query(UserProfile).filter(
        UserProfile.auth_user_id == auth_user_id
    ).first()

    if existing:
        raise HTTPException(status_code=409, detail="Profile already exists")

    profile = UserProfile(
        auth_user_id=auth_user_id,
        **data.model_dump()
    )
    db.add(profile)
    try:
        db.commit()
        db.refresh(profile)
        return profile
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Profile already exists")

def get_profile(db: Session, auth_user_id: int):
    profile = db.query(UserProfile).filter(
        UserProfile.auth_user_id == auth_user_id
    ).first()
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile

def update_profile(db: Session, auth_user_id: int, data: dict):
    profile = get_profile(db, auth_user_id)
    for key, value in data.items():
        setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile

def delete_profile(db: Session, auth_user_id: int):
    profile = get_profile(db, auth_user_id)
    db.delete(profile)
    db.commit()

def deactivate_profile(db: Session, auth_user_id: int):
    profile = get_profile(db, auth_user_id)
    profile.is_active = False
    db.commit()
    db.refresh(profile)
    return profile