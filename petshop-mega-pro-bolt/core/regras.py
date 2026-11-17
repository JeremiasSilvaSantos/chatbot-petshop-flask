"""Plano B sem IA: o mesmo atendimento por palavras-chave que você já tinha."""
import re
import unicodedata

from core.dados import brl


def limpar_texto(texto: str) -> str:
    norm = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in norm if not unicodedata.combining(c)).lower().strip()


def _tem(texto: str, palavras: list[str], exato: bool = False) -> bool:
    """Casa por palavra inteira (antes, 'oi' disparava em 'noite' e 'ola' em 'escola')."""
    fim = r"\b" if exato else r"\w*"
    return any(re.search(r"\b" + re.escape(p) + fim, texto) for p in palavras)


def responder_por_regras(mensagem: str, db: dict) -> str:
    t = limpar_texto(mensagem)
    v = db["valores"]

    if _tem(t, ["urgente", "emergencia", "socorro", "passando mal", "machucou", "sangrando"]):
        return (
            "🚨 **ATENÇÃO: SEU PET PRECISA DE AJUDA URGENTE!** 🚨\n\n"
            "Mantenha a calma! Nossa equipe veterinária de plantão está pronta para receber vocês. Não espere o chat!\n\n"
            f"1. Venha direto para: {db['endereco']}\n"
            f"2. Se preferir avisar no caminho, ligue: **{db['telefone_fixo']}**"
        )

    if _tem(t, ["oi", "ola", "bom dia", "boa tarde", "boa noite", "opa"], exato=True):
        return (
            f"Olá! Que alegria receber sua mensagem na {db['nome']}! 🐾✨\n\n"
            "Eu sou o Bolt, seu assistente virtual. Posso ajudar com estética, horários, localização e produtos.\n\n"
            "Como posso ajudar você e o seu melhor amigo hoje?"
        )

    if _tem(t, ["preco", "valor", "quanto custa", "banho", "tabela", "tosa", "lavar"]):
        r = ("🧼 **Estética Canina & Felina**\n\nTodos os banhos usam shampoo neutro e hipoalergênico e "
             "**já incluem corte de unhas e limpeza de ouvidos!** ❤️\n\n")
        if _tem(t, ["pequeno", "filhote", "shitzu", "poodle", "yorkshire", "pug"]):
            r += f"• **Porte Pequeno:** {brl(v['pequeno'])}"
        elif _tem(t, ["medio", "cocker", "beagle", "frenchie", "bulldog"]):
            r += f"• **Porte Médio:** {brl(v['medio'])}"
        elif _tem(t, ["grande", "golden", "labrador", "pastor", "husky"]):
            r += f"• **Porte Grande:** {brl(v['grande'])}"
        elif _tem(t, ["gato", "felino", "bichano", "miau"]):
            r += f"• **Gatos:** {brl(v['gato'])} (sala exclusiva e silenciosa para felinos)"
        else:
            extras = "\n".join(f"• {s}" for s in db["servicos_extra"])
            r += (f"• Pequeno: {brl(v['pequeno'])}\n• Médio: {brl(v['medio'])}\n"
                  f"• Grande: {brl(v['grande'])}\n• Gatos: {brl(v['gato'])}\n\n"
                  f"✨ **Serviços adicionais:**\n{extras}")
        r += f"\n\n💡 Pagando no **PIX** você ganha **{db['desconto_pix']}% de desconto**! Deseja agendar?"
        return r

    if _tem(t, ["horario", "funciona", "aberto", "que horas", "domingo", "sabado"]):
        return (f"📅 **Horário de atendimento:**\n{db['horarios']}\n\n"
                "Precisa deixar seu pet bem cedinho? Avise a recepção pelo WhatsApp!")

    if _tem(t, ["onde fica", "localizacao", "endereco", "rua", "bairro", "mapa"]):
        return f"📍 **Endereço:** {db['endereco']}"

    if _tem(t, ["whatsapp", "contato", "humano", "telefone", "falar com alguem", "atendente"]):
        return (f"Claro! Para agendar, confirmar consulta ou tirar dúvidas, fale com a nossa equipe:\n\n"
                f"💬 **WhatsApp:** {db['whatsapp']}\n📞 **Telefone fixo:** {db['telefone_fixo']}")

    if _tem(t, ["obrigado", "obrigada", "valeu", "perfeito", "show", "obg"], exato=True):
        return "Au au! Estamos sempre à disposição para cuidar do seu companheiro de quatro patas. 🐶🐱"

    return ("Hmm, não entendi bem. 🐾 Tente perguntar sobre:\n"
            "• 💰 valor do banho (ex.: porte pequeno)\n• ⏰ horários\n• 📍 endereço\n• 📞 WhatsApp")
