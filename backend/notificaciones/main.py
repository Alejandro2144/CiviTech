from fastapi import FastAPI
from routers import *

app = FastAPI(title="Notificaciones - CiviTech")

app.include_router(notificationsRouter)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Civitech FastAPI project!"}
