from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.config import engine, Base
from app.deps import get_db
from app.repositories import UserRepository
from app.schemas import UserInSchema, AuthDataSchema
from app.utils import create_auth_tokens


app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
async def startup():
    """Create DB tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.exception_handler(IntegrityError)
async def handle_integrity_error(_, exc: IntegrityError):
    """Catch SQLAlchemy errors"""
    err = exc.args[-1].split('\n')[-1]
    return JSONResponse(
        status_code=418,
        content={"message": f"Ошибка. {err}"},
    )


@app.get('/register', response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get('/login', response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/api/register", response_model=AuthDataSchema)
async def create_user(user: UserInSchema, Authorize: AuthJWT = Depends(),
                      db: AsyncSession = Depends(get_db)):
    users = UserRepository(db)
    user = await users.create_user(**user.dict())
    return AuthDataSchema(user=user, tokens=create_auth_tokens(Authorize, user.email))


@app.post("/api/login", response_model=AuthDataSchema)
async def authorize_user(user: UserInSchema, Authorize: AuthJWT = Depends(),
                         db: AsyncSession = Depends(get_db)):
    users = UserRepository(db)
    user = await users.authorize(**user.dict())
    return AuthDataSchema(user=user, tokens=create_auth_tokens(Authorize, user.email))
