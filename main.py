import os
import asyncio
import discord
from discord.ext import commands
from flask import Flask, request
from flask_cors import CORS
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
CORS(app) 

WEBHOOK_URL = "https://discord.com/api/webhooks/1389844080741060678/uaV4LqiNV6cTZrHl_LsN87M76_C6Ml2vU0J9trt0WD_o_GpMnKVXUIjmD8pJVNgnIkja"
CLAVE_SECRETA = "baSLsVSrMMfxlfAdleg6Lqey9N5G"  # ! Cámbiala a algo fuerte

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
