from fastapi import FastAPI
from routers import token

app = FastAPI(title="Token Microservice - CiviTech")

app.include_router(token.router)
