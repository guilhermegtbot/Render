from flask import Flask, request, render_template, jsonify
import subprocess
import os

app = Flask(__name__)

# Configure sua chave de API do Meraki como uma variável de ambiente
MERAKI_API_KEY = os.environ.get("MERAKI_API_KEY")
MERAKI_BASE_URL = "https://api.meraki.com/api/v1"

def get_device_status_curl(device_id):
    """Busca o status de um dispositivo Meraki usando curl."""
    headers = f"'X-Cisco-Meraki-API-Key: {MERAKI_API_KEY}'"
    url = f"{MERAKI_BASE_URL}/devices/{device_id}/status"
    command = [
        "curl",
        "-H", headers,
        url
    ]
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if stderr:  # Verifica se houve algum erro no processo do curl
            return {"error": f"Erro ao executar curl: {stderr.decode('utf-8')}"}
        return jsonify(stdout.decode('utf-8')) # Tenta retornar já como JSON
    except Exception as e:
        return {"error": f"Erro ao executar curl: {e}"}

@app.route("/", methods=["GET"])
def index():
    if request.args.get("device_id"): # Alterado para request.args
        device_id = request.args.get("device_id") # Pega o device_id da query string
        device_info = get_device_status_curl(device_id)
        return render_template("index.html", device_info=device_info, device_id=device_id)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
