import random
import time
import requests
from datetime import datetime

# Simula sensor de temperatura
def gerar_temperatura():
    return round(random.uniform(20.0, 85.0), 2)  # inclui valores altos p/ testar alerta

# Envia temperatura para o servidor Flask
def enviar_temperatura(temperatura):
    url = "http://127.0.0.1:5000/api/temperatura"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    dados = {
        "temperatura": temperatura,
        "timestamp": timestamp
    }

    try:
        r = requests.post(url, json=dados)
        print(f"[{timestamp}] Enviado: {temperatura}°C | Status:", r.status_code)
    except Exception as e:
        print("Erro:", e)


while True:
    temp = gerar_temperatura()
    enviar_temperatura(temp)
    time.sleep(10)
