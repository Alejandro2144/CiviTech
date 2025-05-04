from fastapi import FastAPI
from app.routers import example

app = FastAPI(
    title="CiviTech",
    description="This project is intended to the Civitech project for advanced software architectures.",
    version="0.1.0",
)

app.include_router(example.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Civitech FastAPI project!"}
