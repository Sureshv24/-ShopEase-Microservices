import re
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator

class UserProfileCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    phone_number: str = Field(min_length=7, max_length=20)
    date_of_birth: date | None = None
    gender: str | None = Field(default=None, max_length=30)
    profile_image: str | None = Field(default=None, max_length=500)

    @field_validator("full_name")
    @classmethod
    def clean_name(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Full name cannot be empty")
        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, value):
        value = value.strip()
        if not re.fullmatch(r"\+?[0-9\s\-()]{7,20}", value):
            raise ValueError("Invalid phone number")
        return value

class UserProfileUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=120)
    phone_number: str | None = Field(default=None, min_length=7, max_length=20)
    date_of_birth: date | None = None
    gender: str | None = Field(default=None, max_length=30)
    profile_image: str | None = Field(default=None, max_length=500)

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, value):
        if value is not None and not re.fullmatch(r"\+?[0-9\s\-()]{7,20}", value.strip()):
            raise ValueError("Invalid phone number")
        return value.strip() if value else value

class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    auth_user_id: int
    full_name: str
    phone_number: str
    date_of_birth: date | None
    gender: str | None
    profile_image: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

class MessageResponse(BaseModel):
    message: str