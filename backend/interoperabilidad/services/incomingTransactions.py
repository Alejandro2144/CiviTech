from fastapi import HTTPException, status
import httpx
from constants import GOV_CARPETA_BASEURL, CIVITECH_CONFIRMATION_API
from models import *
from schemas import *

# Get the list of active external operators

