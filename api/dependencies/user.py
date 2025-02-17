from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User

from typing import Optional
from sqlalchemy import select


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result


async def create_user(db: AsyncSession, email: str, hashed_password: str) -> User:
    db_user = User(email=email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
