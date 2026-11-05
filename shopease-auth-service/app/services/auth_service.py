from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.auth_schema import RegisterRequest
from app.core.security import hash_password, verify_password

def register_user(db: Session, data: RegisterRequest):
    email = str(data.email).lower()

    if data.password != data.confirm_password:
        raise ValueError("Password and confirm password do not match")

    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        raise ValueError("Email is already registered")

    user = User(
        full_name=data.full_name,
        email=email,
        password_hash=hash_password(data.password),
        role="customer",
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(
        User.email == email.lower()
    ).first()

    if not user or not verify_password(password, user.password_hash):
        return None

    if not user.is_active:
        return None

    return user
