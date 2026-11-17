import os
os.environ.pop("ANTHROPIC_API_KEY", None)  # testa o modo sem IA

from app import app


def _post(msg):
    return app.test_client().post("/api/chat", json={"history": [{"role": "user", "content": msg}]})


def test_home_renderiza_produtos():
    r = app.test_client().get("/")
    assert r.status_code == 200 and "Ração Premium" in r.get_data(as_text=True)


def test_health():
    assert app.test_client().get("/health").get_json()["status"] == "ok"


def test_preco_pequeno():
    assert "R$ 50,00" in _post("quanto custa o banho do meu poodle?").get_json()["response"]


def test_noite_nao_vira_saudacao():
    assert "Olá!" not in _post("vocês abrem à noite? qual o horário").get_json()["response"]


def test_mensagem_invalida():
    assert app.test_client().post("/api/chat", json={}).status_code == 400
