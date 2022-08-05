from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base


class Settings(BaseModel):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/kalik"
    authjwt_secret_key: str = "secret"


@AuthJWT.load_config
def get_config():
    return Settings()


engine = create_async_engine(Settings().DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()
