from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user_model import UserProfile
from app.models.address_model import UserAddress

def require_profile(db: Session, auth_user_id: int):
    profile = db.query(UserProfile).filter(
        UserProfile.auth_user_id == auth_user_id
    ).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Create your profile first")
    if not profile.is_active:
        raise HTTPException(status_code=403, detail="User profile is inactive")
    return profile

def get_owned_address(db: Session, profile_id: int, address_id: int):
    address = db.query(UserAddress).filter(
        UserAddress.id == address_id,
        UserAddress.user_id == profile_id
    ).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

def clear_default(db: Session, profile_id: int):
    db.query(UserAddress).filter(
        UserAddress.user_id == profile_id,
        UserAddress.is_default.is_(True)
    ).update({"is_default": False}, synchronize_session="fetch")

def create_address(db: Session, profile_id: int, data: dict):
    if data.get("is_default"):
        clear_default(db, profile_id)
    address = UserAddress(user_id=profile_id, **data)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address

def update_address(db: Session, profile_id: int, address_id: int, data: dict):
    address = get_owned_address(db, profile_id, address_id)
    if data.get("is_default") is True:
        clear_default(db, profile_id)
    for key, value in data.items():
        setattr(address, key, value)
    db.commit()
    db.refresh(address)
    return address

def set_default_address(db: Session, profile_id: int, address_id: int):
    address = get_owned_address(db, profile_id, address_id)
    clear_default(db, profile_id)
    address.is_default = True
    db.commit()
    db.refresh(address)
    return address

def delete_address(db: Session, profile_id: int, address_id: int):
    address = get_owned_address(db, profile_id, address_id)
    db.delete(address)
    db.commit()