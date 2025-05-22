import requests
import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv("wpToken.env")

# Token de autenticação do WhatsApp Cloud API
token = os.getenv("WHATSAPP_TOKEN")

# Endpoint da API do WhatsApp
url = "https://graph.facebook.com/v22.0/630293736839982/messages"

# Cabeçalhos HTTP
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

data = {
    "messaging_product": "whatsapp",
    "to": "5511975865004",  # com DDI e DDD
    "type": "template",
    "template": {
        "name": "confirmar_consulta",  # nome do modelo aprovado na Meta
        "language": { "code": "pt_BR" },
        "components": [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": "João da Silva"},
                    {"type": "text", "text": "16/05/2025"},
                    {"type": "text", "text": "14:30"},
                    {"type": "text", "text": "Mariana Cardoso"}
                ]
            }
        ]
    }
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    print("✅ Mensagem enviada com sucesso!")
else:
    print("❌ Erro ao enviar mensagem:")
    print(response.status_code)
    print(response.text)
