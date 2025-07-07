import os
import json
import threading
import requests
import discord
from discord.ext import commands
from flask import Flask, request
from flask_cors import CORS

# ===================== 🔧 CONFIGURACIÓN ======================

TOKEN = os.getenv("DISCORD_TOKEN")
WEBHOOK_URL = os.getenv("LINK")
CLAVE_SECRETA = "baSLsVSrMMfxlfAdleg6Lqey9N5G"

URL_JSON = "https://raw.githubusercontent.com/temporaltime93/bot/refs/heads/main/valor.json"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ===================== 🤖 BOT DE DISCORD ======================

def embed(titulo, descripcion):
    e = discord.Embed(
        title=titulo,
        description=descripcion,
        color=discord.Color.green()
    )
    e.set_image(url="https://firebasestorage.googleapis.com/v0/b/fotos-b8a54.appspot.com/o/Slide%2016_9%20-%204%20(1)%20(1)-min.jpg?alt=media&token=ff085a8b-21ad-4052-9950-16eec59212cd")
    return e

@bot.event
async def on_ready():
    print(f"🤖 Bot conectado como {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

@bot.command(name='borrar')
@commands.has_permissions(manage_messages=True)
async def borrar(ctx, cantidad: int):
    if cantidad < 1 or cantidad > 100:
        await ctx.send("❌ Número entre 1 y 100 por favor.")
        return
    await ctx.message.delete()
    borrados = await ctx.channel.purge(limit=cantidad)
    await ctx.send(embed=embed("🧹 BORRADO", f"Se borraron **{len(borrados)}** mensajes."), delete_after=5)

@bot.command(name="ID")
async def ID(ctx):
    user_id = ctx.author.id
    username = ctx.author.name
    e = discord.Embed(
        title="👤 Tu ID de usuario",
        description=f"Hola **{username}**, tu ID es: `{user_id}`",
        color=discord.Color.green()
    )
    await ctx.send(embed=e)

# ===================== 🌐 API FLASK ======================

app = Flask(__name__)
CORS(app)

def mensaje(placeNb, Name_user, Informacion):
    try:
        response = requests.get(URL_JSON)
        response.raise_for_status()
        valores = response.json()
    except Exception as e:
        return f"❌ Error al obtener JSON remoto: {e}", 500

    if placeNb not in valores:
        return f"❌ La clave '{placeNb}' no está registrada en valor.json", 400

    ID = valores[placeNb]["ID"]
    ST = valores[placeNb]["SCRIPT"]

    EMBEB = {
        "content": f"# Holiiiii...! <@{Name_user}>",
        "allowed_mentions": {"users": [Name_user]},
        "embeds": [
            {
                "title": "Holiiiii...!",
                "description": f"""```ansi
[2;35m[1;35mVengo a avisarte por parte del script("{ST}") para decirte que:[0m

[2;34m[1;34m[1;40m----------->

{Informacion}

----------->[0m

[2;35m¡Bueno, eso era todo, bye! No olvides de recomendarnos con tus amigos shiii~[0m
```""",
                "color": 16121600,
                "image": {
                    "url": "https://firebasestorage.googleapis.com/v0/b/fotos-b8a54.appspot.com/o/9f0db6ff6c059e1d14b1f37b69f55c21%201.png?alt=media&token=76744d86-5e4a-4676-8461-ea5095916b4e"
                }
            }
        ],
    }

    try:
        resp = requests.post(WEBHOOK_URL, json=EMBEB, params={"thread_id": ID})
        if resp.status_code in (200, 204):
            return "✅ Mensaje enviado al hilo de Discord", 200
        else:
            return f"❌ Error al enviar mensaje: {resp.status_code}\n{resp.text}", 500
    except Exception as e:
        return f"❌ Error en el servidor: {str(e)}", 500

@app.route("/enviar", methods=["GET"])
def enviar():
    clave = request.args.get("Nkart", "")
    _placeNb_ = request.args.get("IPFUEOPjd", "")
    _Name_user_ = request.args.get("davvgfrF", "")
    _Informacion_ = request.args.get("OIHDoihio", "")

    if clave != CLAVE_SECRETA:
        return "❌ Clave incorrecta. No autorizado.", 403

    return mensaje(_placeNb_, _Name_user_, _Informacion_)

# ===================== 🚀 INICIAR BOT Y API ======================

def run_flask():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.run(TOKEN)
