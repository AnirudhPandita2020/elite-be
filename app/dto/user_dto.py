from datetime import datetime

from pydantic import BaseModel, EmailStr


class CreateUserDto(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserModel(BaseModel):
    email: EmailStr
    name: str
    authority_level = int
    created_at: datetime
    is_active: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    type: str
