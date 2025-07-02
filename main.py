import os
import asyncio
import discord
from discord.ext import commands
from flask import Flask, request
import requests
import threading

# ========== Configuración del BOT ==========
TOKEN = os.getenv("DISCORD_TOKEN")  # Asegúrate de definirla en el entorno

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

import comandos_bot
comandos_bot.setup(bot)

# ========== Configuración de Flask ==========
app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1387516322941894686/EwHdpFHRis-BkgFLh7f9tHUBUB3REd_-qcr9yHgT4aaZu3CSs0NhH266LBAOmB8cKftB"
CLAVE_SECRETA = "midiscordkey2025"  # ! Cámbiala a algo fuerte

@app.route("/enviar", methods=["GET"])
def enviar():
    mensaje = request.args.get("mensaje", "")
    clave = request.args.get("clave", "")

    if clave != CLAVE_SECRETA:
        return "❌ Clave incorrecta. No autorizado.", 403

    if not mensaje.strip():
        return "⚠️ Mensaje vacío. No se envió nada.", 400

    contenido = {"content": mensaje, "username": "Webhook desde GET"}
    requests.post(WEBHOOK_URL, json=contenido)
    return "✅ Mensaje enviado a Discord", 200

# ========== Ejecutar Flask y el Bot ==========
def run_flask():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.run(TOKEN)
