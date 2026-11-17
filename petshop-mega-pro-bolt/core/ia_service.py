"""Bolt: por padrão responde só por regras (custo zero). A IA é opcional: exige ANTHROPIC_API_KEY + requirements-ia.txt."""
import logging
import os

from core.prompt_mestre import PromptMestre
from core.regras import responder_por_regras

log = logging.getLogger("bolt")


class BoltService:
    def __init__(self, db: dict):
        self.db = db
        self.system = PromptMestre(db).get_prompt()
        self.modelo = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
        self.client = None
        if os.getenv("ANTHROPIC_API_KEY"):
            try:
                from anthropic import Anthropic
                self.client = Anthropic(timeout=20.0, max_retries=1)
            except ImportError:
                log.warning("Pacote 'anthropic' não instalado; usando só as regras (sem IA)")

    @property
    def modo(self) -> str:
        return "ia" if self.client else "regras"

    def responder(self, historico: list[dict]) -> str:
        if self.client:
            try:
                msgs = list(historico)
                while msgs and msgs[0]["role"] != "user":
                    msgs.pop(0)
                resp = self.client.messages.create(
                    model=self.modelo, max_tokens=400, system=self.system, messages=msgs
                )
                texto = "".join(b.text for b in resp.content if b.type == "text").strip()
                if texto:
                    return texto
            except Exception:
                log.exception("Falha na IA; usando respostas por regras")
        return responder_por_regras(historico[-1]["content"], self.db)
