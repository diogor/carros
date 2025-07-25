from fastapi import FastAPI
from .routes import veiculos_router

app = FastAPI()

app.include_router(veiculos_router)
