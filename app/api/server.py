from fastapi import FastAPI
from database.sqlmodel import setup_database
from .routes import veiculos_router

app = FastAPI()

setup_database()

app.include_router(veiculos_router)
