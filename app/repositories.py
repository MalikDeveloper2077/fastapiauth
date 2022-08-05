from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserSchema
from app.utils import hash_password, verify_password


class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_user(self, email: str, password: str) -> UserSchema:
        user = User(email=email, password=hash_password(password))
        self.db_session.add(user)
        await self.db_session.flush()
        self.db_session.refresh(user)
        return UserSchema(id=user.id, email=user.email)

    async def authorize(self, email: str, password: str) -> UserSchema:
        """Authenticate user and return JWT tokens with the user data"""
        user_query = await self.db_session.execute(
            select(User).where(User.email == email)
        )

        try:
            user = user_query.scalars().all()[0]
            assert verify_password(password, user.password)
        except IndexError:
            raise HTTPException(400, detail='Пользователь не найден')
        except AssertionError:
            raise HTTPException(400, detail='Неверный пароль')

        return UserSchema(id=user.id, email=user.email)
