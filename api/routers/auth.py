import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_db
from schemas.auth import UserCreate, Token
from core.security import create_access_token, get_password_hash, verify_password
from models.user import User

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
async def register(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).filter(User.email == user_create.email))
        user = result.scalar_one_or_none()
        if user:
            raise HTTPException(status_code=400, detail="Email already in use")

        hashed_password = get_password_hash(user_create.password)

        token_data = {"sub": user_create.email}
        access_token = create_access_token(data=token_data)

        new_user = User(
            email=user_create.email,
            hashed_password=hashed_password,
            jwt=access_token
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        logger.error(f"Ошибка в /register: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Server error")


@router.post("/login", response_model=Token)
async def login(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).filter(User.email == user_create.email))
        user = result.scalar_one_or_none()
        if not user or not verify_password(user_create.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect email password")

        access_token = create_access_token(data={"sub": user.email})
        user.jwt = access_token
        await db.commit()

        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        logger.error(f"Ошибка в /login: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Server error")
