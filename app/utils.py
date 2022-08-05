from fastapi_jwt_auth import AuthJWT
from passlib.context import CryptContext

from app.schemas import AuthTokensSchema


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_auth_tokens(Authorize: AuthJWT, subject: str | int) -> AuthTokensSchema:
    """Create a pair of tokens by fastapi jwt library"""
    return AuthTokensSchema(
        access=Authorize.create_access_token(subject=subject),
        refresh=Authorize.create_refresh_token(subject=subject)
    )


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)
