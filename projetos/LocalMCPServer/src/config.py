import os
from pathlib import Path

from dotenv import load_dotenv


# Carrega as variáveis do arquivo .env
load_dotenv()


# Diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent


# Caminho dos documentos
DOCUMENTS_PATH = os.getenv(
    "DOCUMENTS_PATH",
    "./data/documents"
)


# Converte o caminho relativo para absoluto
DOCUMENTS_DIR = (BASE_DIR / DOCUMENTS_PATH).resolve()


# Garante que o diretório exista
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)