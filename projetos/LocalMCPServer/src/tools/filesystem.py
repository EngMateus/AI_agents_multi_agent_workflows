from pathlib import Path

from src.config import DOCUMENTS_DIR


def list_files() -> list[str]:
    """
    Lista os arquivos disponíveis no diretório de documentos.
    """

    files = []

    for file_path in DOCUMENTS_DIR.rglob("*"):
        if file_path.is_file():
            relative_path = file_path.relative_to(DOCUMENTS_DIR)
            files.append(str(relative_path))

    return files


def read_file(filename: str) -> str:
    """
    Lê o conteúdo de um arquivo.
    """

    file_path = (DOCUMENTS_DIR / filename).resolve()

    # Garante que o arquivo está dentro do diretório permitido
    if not file_path.is_relative_to(DOCUMENTS_DIR):
        raise ValueError("Acesso ao arquivo não permitido.")

    if not file_path.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {filename}"
        )

    if not file_path.is_file():
        raise ValueError(
            f"O caminho informado não é um arquivo: {filename}"
        )

    return file_path.read_text(encoding="utf-8")


def search_files(query: str) -> list[dict]:
    """
    Procura uma determinada palavra ou expressão
    dentro dos arquivos de texto.
    """

    results = []

    query = query.lower()

    for file_path in DOCUMENTS_DIR.rglob("*"):

        if not file_path.is_file():
            continue

        try:
            content = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for line_number, line in enumerate(
            content.splitlines(),
            start=1
        ):

            if query in line.lower():

                results.append(
                    {
                        "file": str(
                            file_path.relative_to(DOCUMENTS_DIR)
                        ),
                        "line": line_number,
                        "content": line.strip(),
                    }
                )

    return results