from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import documents_router

app = FastAPI(title="Documentos - CiviTech")

# 🚨 CORS para permitir peticiones desde el frontend (React Vite)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Civitech FastAPI project!"}
