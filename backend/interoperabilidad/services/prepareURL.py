from fastapi import HTTPException, status
import httpx
from constants import GOV_CARPETA_BASEURL, CIVITECH_CONFIRMATION_API
from schemas import *

def prepareURLDocuments(urlDict: dict):

    """
    Extrae las URLs de los documentos en 'data' y las devuelve
    en un diccionario con claves 'URL1', 'URL2', ...
    
    :param data: dict con clave "documents" conteniendo una lista de dicts
    :return: dict {'URL1': url1, 'URL2': url2, ...}
    """
    urls = {}

    for idx, doc in enumerate(urlDict.get("documents", []), start=1):

        key = f"URL{idx}"
        # Asumimos que 'urlDocument' siempre existe en cada doc
        urls[key] = doc["urlDocument"]

    return urls