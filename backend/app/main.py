from fastapi import FastAPI

from app.api.api_router import api_router

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
