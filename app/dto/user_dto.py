from pydantic import BaseModel, EmailStr


class CreateUserDto(BaseModel):
    email: EmailStr
    password: str
    name: str
