import os
import asyncio
from aioweb import web  # Biblioteca para criar um mini servidor web gratuito
from discord.ext import commands
import discord

# Configuração do Bot do Discord
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    # Tenta carregar a cog da Gun Van
    try:
        await bot.load_extension("cogs.gunvan")
        print("Cog da Gun Van carregada com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar cog: {e}")

# --- MINI SERVIDOR WEB PARA O RENDER ---
async def handle(request):
    return web.Response(text="Bot da Gun Van está online e pronto!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # O Render exige que usemos a porta que ele define na variável 'PORT'
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Servidor web rodando na porta {port}")

async def main():
    # Inicia o servidor web e o bot ao mesmo tempo
    await start_web_server()
    token = os.getenv("DISCORD_TOKEN")
    if token:
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
