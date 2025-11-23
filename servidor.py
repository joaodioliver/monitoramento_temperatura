from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ---------------------------
# Função para conectar ao BD
# ---------------------------
def conectar_db():
    conn = sqlite3.connect('temperaturas.db', check_same_thread=False)
    return conn

# ---------------------------
# Criar tabela se não existir
# ---------------------------
conn = conectar_db()
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS temperaturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperatura REAL,
    timestamp TEXT
)
""")
conn.commit()


# ---------------------------
# Rota API - Receber temperatura do cliente
# ---------------------------
@app.route('/api/temperatura', methods=['POST'])
def receber_temperatura():
    dados = request.get_json()
    temperatura = dados.get('temperatura')
    timestamp = dados.get('timestamp')

    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO temperaturas (temperatura, timestamp) VALUES (?, ?)",
                   (temperatura, timestamp))
    conn.commit()
    conn.close()

    return jsonify({"message": "Temperatura recebida com sucesso!"})


# ---------------------------
# Rota API - Retornar dados em JSON para o gráfico
# ---------------------------
@app.route('/temperaturas_json')
def temperaturas_json():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT temperatura, timestamp FROM temperaturas ORDER BY id DESC LIMIT 50")
    dados = cursor.fetchall()
    conn.close()

    # Monta JSON para enviar ao Chart.js
    temperaturas = [float(linha[0]) for linha in dados][::-1]
    tempos = [linha[1] for linha in dados][::-1]

    return jsonify({"temperaturas": temperaturas, "tempos": tempos})


# ---------------------------
# Rota do DASHBOARD
# ---------------------------
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


# ---------------------------
# Iniciar servidor
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
