from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Servidor online!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Dados recebidos:", data)
    return jsonify({"status": "recebido"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Padrão para Render
    app.run(host="0.0.0.0", port=port)
