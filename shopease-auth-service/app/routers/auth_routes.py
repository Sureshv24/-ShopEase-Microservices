from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError

from app.database.connection import get_db
from app.models.user_model import User
from app.schemas.auth_schema import (
    RegisterRequest, RegistrationResponse, LoginRequest,
    LoginResponse, UserResponse, TokenVerifyRequest,
    TokenVerifyResponse, ChangePasswordRequest, MessageResponse
)
from app.services.auth_service import register_user, authenticate_user
from app.core.security import (
    create_access_token, get_current_user,
    verify_password, hash_password, decode_access_token
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post(
    "/register",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED
)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = register_user(db, data)
        return {
            "message": "Registration successful",
            "user": user
        }
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, str(data.email), data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token(user)

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/verify-token", response_model=TokenVerifyResponse)
def verify_token(data: TokenVerifyRequest, db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(data.access_token)
        user_id = int(payload.get("sub"))
        user = db.get(User, user_id)

        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="User is inactive or missing")

        return {
            "valid": True,
            "message": "Token is valid",
            "user_id": user.id,
            "role": user.role
        }

    except (JWTError, ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@router.post("/change-password", response_model=MessageResponse)
def change_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(data.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    if data.current_password == data.new_password:
        raise HTTPException(
            status_code=400,
            detail="New password must be different from current password"
        )

    current_user.password_hash = hash_password(data.new_password)
    db.commit()

    return {"message": "Password changed successfully"}
