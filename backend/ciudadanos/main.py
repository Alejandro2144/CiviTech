from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import citizen, set_password, internal_transfer
from config.db import Base, engine

app = FastAPI(title="Ciudadanos - CiviTech")

# 🚨 Configurar CORS para permitir peticiones del frontend
origins = [
    "http://localhost:5173",  
    "http://127.0.0.1:5173",  
    # "https://tudominio.com"  <-- Cuando pases a producción, agrega aquí tu dominio real
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# ✅ Crear tablas automáticamente (en desarrollo)
Base.metadata.create_all(bind=engine)

# ✅ Incluir routers
app.include_router(citizen.router)
app.include_router(set_password.router)
app.include_router(internal_transfer.router)
