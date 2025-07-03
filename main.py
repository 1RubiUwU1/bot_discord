import os
import discord
from discord.ext import commands
from flask import Flask, request
from flask_cors import CORS
import threading
import requests

# ===================== DISCORD BOT ======================
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Función para crear embeds de respuesta
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

@bot.command(name="mi_id")
async def mi_id(ctx):
    user_id = ctx.author.id
    username = ctx.author.name
    await ctx.send(f"👤 Hola **{username}**, tu ID es: `{user_id}`")

@bot.command(name='borrar')
@commands.has_permissions(manage_messages=True)
async def borrar(ctx, cantidad: int):
    if cantidad < 1 or cantidad > 100:
        await ctx.send("❌ Número entre 1 y 100 por favor.")
        return
    await ctx.message.delete()
    borrados = await ctx.channel.purge(limit=cantidad)
    await ctx.send(embed=embed("🧹 BORRADO", f"Se borraron **{len(borrados)}** mensajes."), delete_after=5)

# ===================== FLASK API ========================
app = Flask(__name__)
CORS(app)

WEBHOOK_URL = "https://discord.com/api/webhooks/1389844080741060678/uaV4LqiNV6cTZrHl_LsN87M76_C6Ml2vU0J9trt0WD_o_GpMnKVXUIjmD8pJVNgnIkja"
CLAVE_SECRETA = "baSLsVSrMMfxlfAdleg6Lqey9N5G"

PING_ID = {
    "AUTO_BONOS": {
        "ID": "1390085681803427971"
    }
}

def mensaje(placeNb, Name_user, script, Informacion):
    GENERAL = PING_ID.get(placeNb, {})
    ID = GENERAL.get("ID", None)
    if not ID:
        return "❌ ID de hilo no encontrado.", 400

    EMBEB = {
        "content": f"<@{Name_user}>",
        "allowed_mentions": {"users": [Name_user]},
        "embeds": [
            {
                "description": f"""```ansi
[2;35m[1;35m
Vengo a avisarte por parte del script(\"{script}\") para decirte que:[0m[2;35m[0m
```
```ansi
[2;34m
------>
{Informacion}
------>[0m
```

```ansi
[2;35m[1;35m¡Bueno, eso era todo, bye! No olvides derecomendarnos con tus amigos shiii~[0m
```""",
                "color": 16121600,
                "image": {
                    "url": "https://firebasestorage.googleapis.com/v0/b/fotos-b8a54.appspot.com/o/9f0db6ff6c059e1d14b1f37b69f55c21%201.png?alt=media&token=76744d86-5e4a-4676-8461-ea5095916b4e"
                }
            }
        ]
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
    clave = request.args.get("clave", "")
    placeNb = request.args.get("placeNb", "")
    Name_user = request.args.get("Name_user", "")
    script = request.args.get("script", "")
    Informacion = request.args.get("Informacion", "")

    if clave != CLAVE_SECRETA:
        return "❌ Clave incorrecta. No autorizado.", 403

    if not all([placeNb, Name_user, script, Informacion]):
        return "⚠️ Faltan parámetros.", 400

    return mensaje(placeNb, Name_user, script, Informacion)

# ===================== EJECUCIÓN MULTIHILO ========================
def run_flask():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.run(TOKEN)
