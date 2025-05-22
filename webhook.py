from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = "whatsapp-webhook-9f2d38a4"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token     = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == VERIFY_TOKEN:
            print("✔️ Webhook verificado!")
            return challenge, 200
        else:
            print("❌ Verificação falhou:", request.args)
            return "Token inválido", 403

    # POST
    data = request.get_json()
    print("📩 Webhook recebido:", data)

    entries = data.get('entry', [])
    for entry in entries:
        changes = entry.get('changes', [])
        for change in changes:
            value = change.get('value', {})
            messages = value.get('messages', [])

            for msg in messages:
                if msg.get('type') == 'button':
                    wa_id = msg.get('from')
                    payload = msg['button'].get('payload', '')
                    text = msg['button'].get('text', '')

                    print(f"\n📲 Resposta de {wa_id}:")
                    print(f"   • payload = {repr(payload)}")
                    print(f"   • texto   = {repr(text)}")

                    # Usa o texto como chave de decisão
                    normalized_text = text.strip().lower()

                    if normalized_text == 'confirmar consulta':
                        print("✅ Consulta confirmada!")
                    elif normalized_text == 'cancelar consulta':
                        print("❌ Consulta cancelada!")
                    else:
                        print("⚠️ Resposta desconhecida:", text)

    return jsonify(status='ok'), 200

if __name__ == '__main__':
    app.run(port=5000)
