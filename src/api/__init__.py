from fastapi import APIRouter

from .users import router as users_router

from .movies import router as movies_router

from .reviews import router as reviews_router
from src.api.basic_auth.views import router as basic_auth_router

router = APIRouter()
router.include_router(users_router)
router.include_router(movies_router)
router.include_router(reviews_router)
router.include_router(basic_auth_router)
