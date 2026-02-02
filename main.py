import discord
from discord.ext import commands
from discord import app_commands
import datetime
import os

# ===============================
# INTENTS
# ===============================

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===============================
# JERARQUÍA DE RANGOS (ORDEN EXACTO)
# ===============================

RANGOS = [
    "Jefe",
    "Subjefe",
    "Capitan principal",
    "Coordinador de operaciones",
    "Supervisor",
    "Sargento",
    "Teniente mayor",
    "Teniente",
    "Ejecutor",
    "Jefe de operaciones",
    "Comandante",
    "Aprendiz comandante",
    "Capitan",
    "Operaciones especiales",
    "Seguridad",
    "Sicario mayor",
    "Puntero mayor",
    "Sicario",
    "Puntero"
]

# ===============================
# DATOS DE SERVICIO
# ===============================

servicios_activos = {}

# ===============================
# EVENTO READY
# ===============================

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot conectado como {bot.user}")

# ===============================
# FUNCIÓN PARA OBTENER RANGO
# ===============================

def obtener_rango(user: discord.Member):
    roles_usuario = [rol.name for rol in user.roles]
    for rango in RANGOS:
        if rango in roles_usuario:
            return rango
    return "Sin rango"

# ===============================
# COMANDO: ENTRAR EN SERVICIO
# ===============================

@bot.tree.command(name="entrar-servicio", description="Entrar en servicio")
async def entrar_servicio(interaction: discord.Interaction):
    user = interaction.user

    if user.id in servicios_activos:
        await interaction.response.send_message(
            "❌ Ya estás en servicio.",
            ephemeral=True
        )
        return

    rango = obtener_rango(user)
    inicio = datetime.datetime.now()

    servicios_activos[user.id] = {
        "inicio": inicio,
        "rango": rango
    }

    embed = discord.Embed(
        title="🟢 EN SERVICIO",
        color=0x2ecc71,
        timestamp=inicio
    )
    embed.add_field(name="👤 Usuario", value=user.mention, inline=False)
    embed.add_field(name="🎖️ Rango", value=rango, inline=True)
    embed.add_field(
        name="⏰ Inicio",
        value=inicio.strftime("%d/%m/%Y %H:%M"),
        inline=True
    )
    embed.set_footer(text="Sistema de Servicio • Mafia RP")

    await interaction.response.send_message(embed=embed)

# ===============================
# COMANDO: SALIR DEL SERVICIO
# ===============================

@bot.tree.command(name="salir-servicio", description="Salir del servicio")
async def salir_servicio(interaction: discord.Interaction):
    user = interaction.user

    if user.id not in servicios_activos:
        await interaction.response.send_message(
            "❌ No estás en servicio.",
            ephemeral=True
        )
        return

    data = servicios_activos.pop(user.id)
    inicio = data["inicio"]
    rango = data["rango"]
    fin = datetime.datetime.now()

    tiempo = fin - inicio
    horas, resto = divmod(int(tiempo.total_seconds()), 3600)
    minutos = resto // 60

    embed = discord.Embed(
        title="🔴 FIN DE SERVICIO",
        color=0xe74c3c,
        timestamp=fin
    )
    embed.add_field(name="👤 Usuario", value=user.mention, inline=False)
    embed.add_field(name="🎖️ Rango", value=rango, inline=True)
    embed.add_field(
        name="⏱️ Tiempo trabajado",
        value=f"{horas}h {minutos}m",
        inline=True
    )
    embed.add_field(
        name="📅 Fecha",
        value=fin.strftime("%d/%m/%Y %H:%M"),
        inline=False
    )
    embed.set_footer(text="Sistema de Servicio • Mafia RP")

    await interaction.response.send_message(embed=embed)

# ===============================
# INICIAR BOT
# ===============================

bot.run(os.getenv("TOKEN"))
