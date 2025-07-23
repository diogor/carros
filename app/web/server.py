from fastapi import FastAPI

app = FastAPI()


@app.get("/", response_model=str)
async def jogo() -> str:
    return "Hello, World"
