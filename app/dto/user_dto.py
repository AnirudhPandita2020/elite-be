from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class CreateUserDto(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserModel(BaseModel):
    email: EmailStr
    name: str
    created_at: datetime
    profile_photo: Optional[str] | None
    is_active: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    type: str
