import json
from pathlib import Path

ARQUIVO = Path(__file__).resolve().parent.parent / "data" / "petshop.json"


def carregar_dados() -> dict:
    with open(ARQUIVO, encoding="utf-8") as f:
        return json.load(f)


def brl(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
