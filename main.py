 import os
import asyncio
from aiohttp import web
from discord.ext import commands
import discord

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

@bot.event
async def on_ready():
    print(f"Bot conectado com sucesso como {bot.user}!")
    try:
        await bot.load_extension("cogs.gunvan")
        print("Cog da Gun Van carregada com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar cog: {e}")

async def handle(request):
    return web.Response(text="Bot da Gun Van está online e rodando!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Servidor web rodando na porta {port}")

async def main():
    # Inicia o servidor web em segundo plano
    web_task = asyncio.create_task(start_web_server())
    
    # Inicia o bot do Discord
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot_task = asyncio.create_task(bot.start(token))
        await asyncio.gather(web_task, bot_task)
    else:
        print("ERRO: Token do Discord não configurado nas variáveis de ambiente.")

if __name__ == "__main__":
    asyncio.run(main())
