from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# ——————————————————————————————————————————————
# 🔐 TOKEN DE VERIFICAÇÃO: deve bater com o da Meta
# ——————————————————————————————————————————————
VERIFY_TOKEN = "whatsapp-webhook-9f2d38a4"

# ——————————————————————————————————————————————
# Rota de saúde (usada pelo Render para checar que o app está vivo)
# ——————————————————————————————————————————————
@app.route("/", methods=["GET"])
def index():
    return "Servidor online!", 200

# ——————————————————————————————————————————————
# Rota de Webhook do WhatsApp
# ——————————————————————————————————————————————
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    # ————————————— Verificação do webhook (GET) —————————————
    if request.method == "GET":
        mode      = request.args.get("hub.mode")
        token     = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        # Confere se o token bate e responde o desafio
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("✔️  Webhook verificado com sucesso!")
            return challenge, 200
        else:
            print("❌  Falha na verificação do webhook:", request.args)
            return "Token inválido", 403

    # ————————————— Recebimento de eventos (POST) —————————————
    data = request.get_json(force=True)
    print("📩  Dados recebidos no webhook:", data)

    # ——————————— Processa possíveis cliques em botões ———————————
    entries = data.get("entry", [])
    for entry in entries:
        for change in entry.get("changes", []):
            value    = change.get("value", {})
            messages = value.get("messages", [])

            for msg in messages:
                # Só tratamos mensagens do tipo 'button'
                if msg.get("type") == "button":
                    from_number = msg.get("from")                     # número do usuário
                    btn_payload = msg["button"].get("payload", "")    # payload enviado
                    btn_text    = msg["button"].get("text", "")       # texto exibido no botão

                    print(f"\n📲 Resposta de {from_number}:")
                    print(f"   • payload = {repr(btn_payload)}")
                    print(f"   • texto   = {repr(btn_text)}")

                    # Normaliza e decide se confirmou ou cancelou
                    normalized = btn_text.strip().lower()
                    if normalized == "confirmar consulta":
                        print("✅ Consulta confirmada!")
                    elif normalized == "cancelar consulta":
                        print("❌ Consulta cancelada!")
                    else:
                        print("⚠️ Resposta desconhecida:", btn_text)

    # Sempre responda 200 para o WhatsApp saber que recebeu
    return jsonify(status="ok"), 200

# ——————————————————————————————————————————————
# Binding para produção (Render, Heroku, etc.)
# ——————————————————————————————————————————————
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # host=0.0.0.0 faz com que o container aceite conexões externas
    app.run(host="0.0.0.0", port=port)
