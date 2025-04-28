from fastapi import FastAPI
from routers.register_router import router as register_router

app = FastAPI(
    title="CiviTech",
    description="This project is intended to the Civitech project for advanced software architectures.",
    version="0.1.0",
)

app.include_router(register_router)

# Para correrlo:
# uvicorn main:app --reload
