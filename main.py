import os
import asyncio
from aiohttp import web  # CORRIGIDO: Biblioteca de servidor web
from discord.ext import commands
import discord

# Configuração do Bot do Discord
intents = discord.Intents.default()
intents.message_content = True # Importante para ler comandos

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
    return web.Response(text="Bot da Gun Van está online!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # O Render define a porta na variável 'PORT', ou usamos 8080
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Servidor web rodando na porta {port}")

async def main():
    # Cria as tarefas do servidor web e do bot
    web_task = asyncio.create_task(start_web_server())
    
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot_task = asyncio.create_task(bot.start(token))
        # Roda os dois juntos
        await asyncio.gather(web_task, bot_task)
    else:
        print("ERRO: Token do Discord não encontrado nas variáveis de ambiente.")

if __name__ == "__main__":
    asyncio.run(main())
