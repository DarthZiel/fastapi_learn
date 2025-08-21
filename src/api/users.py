from fastapi import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.models.user import User
from src.models.db_helper import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.user import UserCreateResponse, UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserCreateResponse)
async def create_user(
    user: UserCreate, db: AsyncSession = Depends(db_helper.session_getter)
):
    result = await db.execute(select(User).filter(User.username == user.username))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Такой пользователь уже есть")

    db_user = User(username=user.username, password=user.password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return UserCreateResponse.model_validate(db_user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(db_helper.session_getter)):
    result = await db.execute(
        select(User).options(selectinload(User.reviews)).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return UserResponse.model_validate(user)


@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(db_helper.session_getter)):
    result = await db.execute(select(User).options(selectinload(User.reviews)))
    users = result.scalars().all()
    return [UserResponse.model_validate(user) for user in users]
