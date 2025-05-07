from fastapi import FastAPI
from routers import *
from models import *
import os

origins = ["*"]

app = FastAPI()

app.include_router(citizenTransfer)
app.include_router(citizenReceiving)
