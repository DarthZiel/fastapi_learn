import secrets

from fastapi import HTTPException
from typing import Annotated

from fastapi.openapi.utils import status_code_ranges
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.user import User
from src.models.db_helper import db_helper

router = APIRouter(prefix="/demo-basic-auth", tags=["DEMO BASIC AUTH"])

security = HTTPBasic()


@router.get("/basic-auth")
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    return {"username": credentials.username, "password": credentials.password}


async def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    db: AsyncSession = Depends(db_helper.session_getter),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=" invalid login or password",
        headers={"WWW-Authenticate": "Basic"},
    )

    result = await db.execute(
        select(User)
        .options(selectinload(User.reviews))
        .where(User.username == credentials.username)
    )
    user = result.scalars().first()
    if user is None:
        raise unauthed_exc

    if not secrets.compare_digest(
        credentials.password,
        user.password,
    ):
        raise unauthed_exc

    return user.username


@router.get("/basic-auth-usernanme")
def demo_basic_auth_user(auth_username: str = Depends(get_auth_user_username)):
    return {"message": f"Hi, {auth_username}", "username": auth_username}
