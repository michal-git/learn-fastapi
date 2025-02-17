from contextlib import asynccontextmanager
from app.core.db import init_db
from fastapi import FastAPI
from app.api.api_router import api_router
from app.core.config import API_V1_STR


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown logic using the lifespan function."""
    print("Initializing database...")
    init_db()
    yield  # The application runs here
    print("Application shutdown...")


app = FastAPI(lifespan=lifespan)


app.include_router(api_router, prefix=API_V1_STR)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
