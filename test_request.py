import requests
import json

url = "http://localhost:8000/test/send"
payload = {
    "channel": "whatsapp",
    "external_id": "5511999999999",
    "content": "Qual o preço do smartphone?"
}

try:
    response = requests.post(url, json=payload)
    print("Status:", response.status_code)
    print("Resposta:", response.json())
except Exception as e:
    print("Erro:", e)