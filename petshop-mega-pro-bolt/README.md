# PetShop Mega Pro Bolt

> **Desenvolvido por:** Jeremias Silva Santos

Chatbot de atendimento para PetShop feito com Flask. Por padrão responde por regras (palavras-chave), **sem nenhum custo**.
Opcionalmente pode usar IA (veja o fim deste arquivo).

## Rodar no seu computador
    python -m venv .venv
    .venv\Scripts\activate            # Linux/Mac: source .venv/bin/activate
    pip install -r requirements.txt
    python app.py                     # abra http://localhost:5000

Testes: `pip install -r requirements-dev.txt` e depois `pytest -q`.

## Editar preços, horários e produtos
Mexa só em `data/petshop.json`. O site e o bot leem dali.

## Subir para o GitHub
    git init
    git add .
    git commit -m "PetShop Bolt"
    git branch -M main
    git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
    git push -u origin main
O `.gitignore` já deixa de fora o `.venv` e o `.env`.
A cada push, o GitHub Actions roda os testes automaticamente (aba "Actions" do repositório).

## Publicar de graça (Render)
1. Crie uma conta em render.com (não pede cartão) e conecte seu GitHub.
2. New > Blueprint > escolha o repositório. O `render.yaml` já configura o plano gratuito.
3. Em alguns minutos o site fica no ar em `https://petshop-bolt.onrender.com` (ou nome parecido).
Cada `git push` atualiza o site sozinho.

Obs.: no plano gratuito o site "dorme" após ~15 min sem acesso e leva cerca de 1 minuto para acordar no próximo acesso.
Abra o link antes de apresentar o trabalho.

## IA (opcional, tem custo)
`pip install -r requirements-ia.txt` e defina `ANTHROPIC_API_KEY` (copie `.env.example` para `.env`).
Se a chave faltar ou a IA falhar, o Bolt volta sozinho para as regras.

---
**Autor:** Jeremias Silva Santos
