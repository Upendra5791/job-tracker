from pydantic import BaseModel, EmailStr
from pydantic import Field

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)

class Config:
    from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str