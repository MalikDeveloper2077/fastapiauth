from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserInSchema(UserBase):
    password: str


class UserSchema(UserBase):
    id: int


class AuthTokensSchema(BaseModel):
    access: str
    refresh: str


class AuthDataSchema(BaseModel):
    user: UserSchema
    tokens: AuthTokensSchema
