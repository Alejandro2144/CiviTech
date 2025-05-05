import os
from dotenv import load_dotenv

load_dotenv()

GOVCARPETA_BASE_URL = os.getenv("GOVCARPETA_BASE_URL")
GOVCARPETA_OPERATOR_ID = os.getenv("GOVCARPETA_OPERATOR_ID")
GOVCARPETA_OPERATOR_NAME = os.getenv("GOVCARPETA_OPERATOR_NAME")
