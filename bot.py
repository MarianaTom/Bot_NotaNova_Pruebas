import discord
import os
from dotenv import load_dotenv
from discord.ext import commands, tasks
import datetime

load_dotenv()
TOKEN = os.getenv("TOKEN")

# IDs nuevos para pruebas
ID_ASISTENCIA = 1389709699301118095
ID_UPDATE = 1389837483327488011

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def cargar_mensaje(nombre_archivo):
    ruta = os.path.join("recordatorios", nombre_archivo)
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')
    enviar_recordatorios.start()  # Inicia la tarea programada al estar listo el bot

@tasks.loop(minutes=1)
async def enviar_recordatorios():
    now = datetime.datetime.now()
    canal_asistencia = bot.get_channel(ID_ASISTENCIA)
    canal_update = bot.get_channel(ID_UPDATE)

    if now.weekday() == 3:  # jueves
        if now.hour == 12 and now.minute == 0:
            mensaje_avance = cargar_mensaje("mensaje_avance.txt")
            if canal_asistencia:
                await canal_asistencia.send(mensaje_avance)

            if canal_update:
                with open("recordatorios/JuntaSemanal.png", "rb") as f:
                    imagen = discord.File(f)
                link = cargar_mensaje("asistenciaJunta.txt")
                mensaje = await canal_update.send("@everyone", file=imagen)
                await mensaje.reply(f"Registra tu asistencia: [Aquí]({link})")

        elif now.hour == 15 and now.minute == 59:
            mensaje_urgente = cargar_mensaje("mensaje_avanceUrgente.txt")
            if canal_asistencia:
                await canal_asistencia.send(mensaje_urgente)

# Los comandos siguen igual
@bot.command()
async def r_avance(ctx):
    canal = bot.get_channel(ID_ASISTENCIA)
    mensaje = cargar_mensaje("mensaje_avance.txt")
    await canal.send(mensaje)
    await ctx.send("✅ Recordatorio de avance enviado.")

@bot.command()
async def r_urgente(ctx):
    canal = bot.get_channel(ID_ASISTENCIA)
    mensaje = cargar_mensaje("mensaje_avanceUrgente.txt")
    await canal.send(mensaje)
    await ctx.send("✅ Recordatorio urgente enviado.")

@bot.command()
async def r_asistencia(ctx):
    canal = bot.get_channel(ID_UPDATE)
    with open("recordatorios/JuntaSemanal.png", "rb") as f:
        imagen = discord.File(f)
    link = cargar_mensaje("asistenciaJunta.txt")
    mensaje = await canal.send("@everyone", file=imagen)
    await mensaje.reply(f"Registra tu asistencia: [Aquí]({link})")
    await ctx.send("✅ Recordatorio de asistencia enviado.")

@bot.command()
async def prueba_final(ctx):
    canal = bot.get_channel(ID_ASISTENCIA)
    if canal:
        await canal.send("🔧 *Probando bot en servidor final. Favor de ignorar este mensaje.*")
        await ctx.send("✅ Mensaje de prueba enviado al canal de asistencia.")
    else:
        await ctx.send("❌ No se encontró el canal de asistencia.")

bot.run(TOKEN)
