from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.security import get_authenticated_user_id
from app.schemas.address_schema import AddressCreate, AddressUpdate, AddressResponse
from app.services.address_service import (
    require_profile, create_address, get_owned_address,
    update_address, set_default_address, delete_address
)
from app.models.address_model import UserAddress

router = APIRouter(prefix="/api/users/addresses", tags=["User Addresses"])

@router.post("", response_model=AddressResponse, status_code=201)
def add_address(
    data: AddressCreate,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    profile = require_profile(db, auth_user_id)
    return create_address(db, profile.id, data.model_dump())

@router.get("", response_model=list[AddressResponse])
def list_addresses(
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    profile = require_profile(db, auth_user_id)
    return db.query(UserAddress).filter(
        UserAddress.user_id == profile.id
    ).order_by(UserAddress.created_at.desc()).all()

@router.get("/{address_id}", response_model=AddressResponse)
def read_address(
    address_id: int,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    profile = require_profile(db, auth_user_id)
    return get_owned_address(db, profile.id, address_id)

@router.put("/{address_id}", response_model=AddressResponse)
def replace_address(
    address_id: int,
    data: AddressCreate,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    profile = require_profile(db, auth_user_id)
    return update_address(db, profile.id, address_id, data.model_dump())

@router.patch("/{address_id}", response_model=AddressResponse)
def partially_update_address(
    address_id: int,
    data: AddressUpdate,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    profile = require_profile(db, auth_user_id)
    return update_address(
        db, profile.id, address_id, data.model_dump(exclude_unset=True)
    )

@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_address(
    address_id: int,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    profile = require_profile(db, auth_user_id)
    delete_address(db, profile.id, address_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{address_id}/default", response_model=AddressResponse)
def make_default_address(
    address_id: int,
    auth_user_id: int = Depends(get_authenticated_user_id),
    db: Session = Depends(get_db)
):
    profile = require_profile(db, auth_user_id)
    return set_default_address(db, profile.id, address_id)