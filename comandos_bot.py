from discord.ext import commands
import discord
import datetime
import os

# Lista de comandos registrados para el embed de ayuda
comandos_registrados = []

# Variable global para almacenar el enlace temporalmente

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


# Función de setup que registra los comandos
def setup(bot):

    # Registrar comandos para ayuda
    crear_comando('BORRAR', 'Borra mensajes del canal.', '!borrar <cantidad>')
    crear_comando("MI ID:", "Saca la id para el script poing","!ID")
    crear_comando('AYUDA:', 'Muestra los comandos disponibles.', '!help')

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
    async def mi_id(ctx):
        user_id = ctx.author.id
        username = ctx.author.name
        await ctx.send(f"👤 Hola **{username}**, tu ID es: `{user_id}`")


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
