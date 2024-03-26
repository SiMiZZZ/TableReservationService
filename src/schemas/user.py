from pydantic import BaseModel, EmailStr, ConfigDict


class UserAuthReturn(BaseModel):
    model_config = ConfigDict(strict=True)

    username: EmailStr
    id: int
    token: str


class UserAuthData(BaseModel):
    username: EmailStr
    password: str

class UserData(BaseModel):
    username: EmailStr
    role: str
    id: int