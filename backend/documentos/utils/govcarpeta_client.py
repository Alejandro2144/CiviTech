import logging
import httpx
from datetime import datetime, timezone
from config.constants import GOVCARPETA_BASE_URL

# Configurar logger
logger = logging.getLogger(__name__)

class GovCarpetaClient:

    @staticmethod
    async def authenticate_document(metadata: dict) -> tuple[str, datetime | None]:
        """
        Autentica un documento en GovCarpeta.
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                payload = {
                    "idCitizen": metadata.get("idCitizen"),
                    "urlDocument": metadata.get("urlDocument"),
                    "documentTitle": metadata.get("documentTitle")
                }
                
                response = await client.put(f"{GOVCARPETA_BASE_URL}/apis/authenticateDocument", json=payload)

            if response.status_code == 200:
                # Autenticación exitosa, generamos nosotros mismos la fecha
                return "authenticated", datetime.now(timezone.utc)
            else:
                return "failed", None

        except Exception as e:
            print(f"[ERROR] Fallo autenticando documento: {e}")
            return "failed", None
