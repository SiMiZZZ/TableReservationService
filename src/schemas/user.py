from pydantic import BaseModel, EmailStr, ConfigDict


class UserAuthReturn(BaseModel):
    model_config = ConfigDict(strict=True)

    email: EmailStr
    id: int
    token: str


class UserAuthData(BaseModel):
    email: EmailStr
    password: str

class UserRegisteredData(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserData(BaseModel):
    email: EmailStr
    role: str
    id: int
    phone_number: str | None
    name: str | None

class NewUserReturn(BaseModel):
    id: int
    email: EmailStr
    role: str
    password: str

class UserCreate(BaseModel):
    name: str
    email: EmailStr
