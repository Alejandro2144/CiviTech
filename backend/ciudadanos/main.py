from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import citizen
from config.db import Base, engine

app = FastAPI(title="Ciudadanos - CiviTech")

# 🚨 Configurar CORS para permitir peticiones del frontend
origins = [
    "http://localhost:5173",  # Frontend Vite (React)
    "http://127.0.0.1:5173",  # Alternativa localhost
    # "https://tudominio.com"  <-- Cuando pases a producción, agrega aquí tu dominio real
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, PUT, DELETE, OPTIONS...)
    allow_headers=["*"],  # Permitir todos los headers (Authorization, Content-Type...)
)

# ✅ Crear tablas automáticamente (en desarrollo)
Base.metadata.create_all(bind=engine)

# ✅ Incluir routers
app.include_router(citizen.router)
