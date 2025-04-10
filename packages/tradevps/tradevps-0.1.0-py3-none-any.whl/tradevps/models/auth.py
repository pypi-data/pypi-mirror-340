from typing import Optional
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    email: EmailStr

class AuthResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class LoginResponse(BaseModel):
    user: User
    token: str
    token_type: str
