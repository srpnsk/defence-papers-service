from fastapi import FastAPI

from app.api.documents import router


app = FastAPI(
    title="Compile Service",
    version="1.0.0",
)

app.include_router(router)