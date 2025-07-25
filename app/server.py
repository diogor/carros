from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from domain.exceptions import BaseException
from database.sqlmodel import setup_database
from .routes import veiculos_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_database()
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(BaseException)
async def exception_handler(_: Request, exc: BaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "code": exc.code},
    )


app.include_router(veiculos_router)
