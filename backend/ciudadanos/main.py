from fastapi import FastAPI
from ciudadanos.routers import citizen
from ciudadanos.config.db import Base, engine

app = FastAPI(title="Ciudadanos - CiviTech")

# Crear tablas automáticamente (solo en dev, luego usar migraciones)
Base.metadata.create_all(bind=engine)

app.include_router(citizen.router)
