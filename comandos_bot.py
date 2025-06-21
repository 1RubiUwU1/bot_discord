from discord.ext import commands
import discord
import firebase_admin
from firebase_admin import credentials, db
import datetime
import os

# Lista de comandos registrados para el embed de ayuda
comandos_registrados = []

# Variable global para almacenar el enlace temporalmente
link_grok = ""

# Registrar comando para ayuda
def crear_comando(nombre, descripcion, uso):
    comandos_registrados.append({
        "nombre": nombre,
        "descripcion": descripcion,
        "uso": uso
    })

# Función para crear embeds de respuesta
def embed(titulo, descripcion):
    e = discord.Embed(
        title=titulo,
        description=descripcion,
        color=discord.Color.green()
    )
    e.set_image(url="https://firebasestorage.googleapis.com/v0/b/fotos-b8a54.appspot.com/o/Slide%2016_9%20-%204%20(1)%20(1)-min.jpg?alt=media&token=ff085a8b-21ad-4052-9950-16eec59212cd")
    return e

# Función para subir enlace a Firebase Realtime Database
def actualizarz(link):
    if not link.startswith("http://") and not link.startswith("https://"):
        return embed("❌ Enlace inválido", "Debe comenzar con `http://` o `https://`")

    try:
        # Inicializar Firebase si no está listo
        if not firebase_admin._apps:
            ruta_credenciales = os.path.join(os.path.dirname(__file__), os.getenv("fire"))
            cred = credentials.Certificate(ruta_credenciales)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://fotos-b8a54-default-rtdb.firebaseio.com/'
            })

        # ? Sobrescribir el nodo 'link1' dentro de 'links'
        ref = db.reference('links/link1')
        ref.set({
            'link': link,
            'fecha_actualizacion': str(datetime.datetime.now())
        })

        return embed("✅ Enlace actualizado correctamente", f"🔗 {link}")

    except Exception as e:
        print("🔥 Error al subir a Firebase:", e)
        return embed("❌ Error al subir a Firebase", str(e))

# Función de setup que registra los comandos
def setup(bot):

    # Registrar comandos para ayuda
    crear_comando('borrar', 'Borra mensajes del canal.', '!borrar <cantidad>')
    crear_comando('link', 'Guarda un enlace para subirlo luego.', '!link <url>')
    crear_comando('actualizar', 'Sube el enlace guardado a Firebase.', '!actualizar')
    crear_comando('ayuda', 'Muestra los comandos disponibles.', '!ayuda')

    @bot.command(name='borrar')
    @commands.has_permissions(manage_messages=True)
    async def borrar(ctx, cantidad: int):
        if cantidad < 1 or cantidad > 100:
            await ctx.send("❌ Número entre 1 y 100 por favor.")
            return
        await ctx.message.delete()
        borrados = await ctx.channel.purge(limit=cantidad)
        await ctx.send(embed=embed("🧹 BORRADO", f"Se borraron **{len(borrados)}** mensajes."), delete_after=5)

    @bot.command(name='link')
    @commands.has_permissions(manage_messages=True)
    async def link(ctx, url: str):
        global link_grok
        if not url.startswith("http://") and not url.startswith("https://"):
            await ctx.send("❌ Usa un enlace válido que comience con `http://` o `https://`.")
            return
        link_grok = url
        await ctx.send(embed=embed("🔗 Enlace recibido", f"El enlace guardado es:\n`{link_grok}`"))

    @bot.command(name='actualizar')
    @commands.has_permissions(manage_messages=True)
    async def actualizar(ctx):
        global link_grok
        if not link_grok:
            await ctx.send("❌ Primero usa el comando `!link <url>` para guardar un enlace.")
            return
        resultado = actualizarz(link_grok)
        await ctx.send(embed=resultado)

    @bot.command(name='ayuda')
    async def ayuda(ctx):
        ayuda_embed = discord.Embed(title="📘 Comandos disponibles", color=discord.Color.green())
        for cmd in comandos_registrados:
            ayuda_embed.add_field(name=f"!{cmd['nombre']}", value=f"{cmd['descripcion']}\nUso: ```diff\n{cmd['uso']}```", inline=False)
        await ctx.send(embed=ayuda_embed)

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ No tienes permiso para usar este comando.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Faltan argumentos para este comando.")
        elif isinstance(error, commands.CommandNotFound):
            pass  # No mostrar error si el comando no existe
        else:
            await ctx.send("❌ Ocurrió un error inesperado.")
            print("🧨 Error:", error)
