import logging
import time
from collections import defaultdict, deque

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

from core.dados import carregar_dados  # noqa: E402
from core.ia_service import BoltService  # noqa: E402

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
DB = carregar_dados()
bolt = BoltService(DB)

# limite simples por IP (protege o custo da IA): 20 mensagens/minuto
_acessos: dict[str, deque] = defaultdict(deque)


def _limitado(ip: str, limite: int = 20, janela: int = 60) -> bool:
    agora = time.time()
    fila = _acessos[ip]
    while fila and agora - fila[0] > janela:
        fila.popleft()
    if len(fila) >= limite:
        return True
    fila.append(agora)
    return False


def _extrair_historico(dados: dict) -> list[dict] | None:
    if isinstance(dados.get("history"), list):
        hist = [
            {"role": m["role"], "content": m["content"].strip()[:1000]}
            for m in dados["history"][-20:]
            if isinstance(m, dict) and m.get("role") in ("user", "assistant")
            and isinstance(m.get("content"), str) and m["content"].strip()
        ]
    elif isinstance(dados.get("message"), str) and dados["message"].strip():  # formato antigo
        hist = [{"role": "user", "content": dados["message"].strip()[:1000]}]
    else:
        return None
    return hist if hist and hist[-1]["role"] == "user" else None


@app.get("/")
def home():
    return render_template("index.html", db=DB)


@app.get("/health")
def health():
    return jsonify(status="ok", modo=bolt.modo)


@app.post("/api/chat")
def chat_api():
    if _limitado(request.remote_addr or "?"):
        return jsonify(response="Muitas mensagens seguidas. Aguarde um instante e tente de novo. 🐾"), 429
    historico = _extrair_historico(request.get_json(silent=True) or {})
    if not historico:
        return jsonify(response="Mensagem inválida."), 400
    try:
        return jsonify(response=bolt.responder(historico))
    except Exception:
        app.logger.exception("Erro no chat")
        return jsonify(response="⚠️ Tive um probleminha técnico. Tente novamente em instantes."), 500


if __name__ == "__main__":
    app.run(debug=False, port=5000)
