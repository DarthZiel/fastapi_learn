from fastapi import FastAPI
import uvicorn
from src.api import router as api_router
from src.config import settings

app = FastAPI()
app.include_router(api_router, prefix=settings.api_prefix.prefix)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
