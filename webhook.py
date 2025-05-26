from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# -----------------------
# Token de verificação
# -----------------------
VERIFY_TOKEN = "whatsapp-webhook-9f2d38a4"

# -----------------------
# Healthcheck (opcional)
# -----------------------
@app.route("/", methods=["GET"])
def index():
    return "Servidor online!", 200

# -----------------------
# Webhook do WhatsApp
# -----------------------
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    # --- GET: handshake de verificação ---
    if request.method == "GET":
        mode      = request.args.get("hub.mode")
        token     = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("✔️ Webhook verificado com sucesso!")
            return challenge, 200
        else:
            print("❌ Falha na verificação:", request.args)
            return "Token inválido", 403

    # --- POST: recebendo eventos (botões, mensagens etc.) ---
    data = request.get_json()
    print("📩 Evento recebido:", data)

    # (exemplo de como capturar respostas de botão)
    entries = data.get("entry", [])
    for entry in entries:
        for change in entry.get("changes", []):
            value    = change.get("value", {})
            messages = value.get("messages", [])

            for msg in messages:
                if msg.get("type") == "button":
                    user = msg.get("from")
                    txt  = msg["button"].get("text", "")
                    print(f"📲 {user} clicou em '{txt}'")
    return jsonify(status="ok"), 200

# -----------------------
# Binding para produção
# -----------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
