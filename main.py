from flask import Flask, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Permitir llamadas desde JS externo (localhost, etc.)

WEBHOOK_URL = "https://discord.com/api/webhooks/1389844080741060678/uaV4LqiNV6cTZrHl_LsN87M76_C6Ml2vU0J9trt0WD_o_GpMnKVXUIjmD8pJVNgnIkja"
CLAVE_SECRETA = "baSLsVSrMMfxlfAdleg6Lqey9N5G"
THREAD_ID = "1390076717615419575"  # ID del hilo

@app.route("/enviar", methods=["GET"])
def enviar():
    mensaje = request.args.get("mensaje", "")
    clave = request.args.get("clave", "")

    if clave != CLAVE_SECRETA:
        return "❌ Clave incorrecta. No autorizado.", 403

    if not mensaje.strip():
        return "⚠️ Mensaje vacío. No se envió nada.", 400

    contenido = {
        "content": mensaje,
    }

    try:
        # Enviar mensaje al hilo usando el parámetro `thread_id`
        resp = requests.post(WEBHOOK_URL, json=contenido, params={"thread_id": THREAD_ID})

        if resp.status_code in (200, 204):
            return "✅ Mensaje enviado al hilo de Discord", 200
        else:
            return f"❌ Error al enviar mensaje: {resp.status_code}\n{resp.text}", 500
    except Exception as e:
        return f"❌ Error en el servidor: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
