from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def great(name: str = "World"):
    return {f"hello, {name.title()}"}
