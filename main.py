import os
import asyncio
from aiohttp import web
from discord.ext import commands
import discord

# Servidor web para o Render manter o serviço ativo
async def handle(request):
    return web.Response(text="Bot da Gun Van online!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Servidor web rodando na porta {port}")

# Configuração do Bot do Discord
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}!")
    try:
        # Carrega APENAS a cog da Gun Van
        await bot.load_extension("cogs.gunvan")
        print("Cog da Gun Van carregada com sucesso!")

        # Sincroniza os comandos no seu servidor
        GUILD_ID = discord.Object(id=1529337265019551879) 
        bot.tree.clear_commands(guild=GUILD_ID)
        bot.tree.copy_global_to(guild=GUILD_ID)
        synced = await bot.tree.sync(guild=GUILD_ID)
        print(f"Comandos sincronizados: {len(synced)}")
        
    except Exception as e:
        print(f"Erro ao carregar a cog da Gun Van: {e}")

async def main():
    web_task = asyncio.create_task(start_web_server())
    
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("ERRO: DISCORD_TOKEN não configurado!")
        return

    bot_task = asyncio.create_task(bot.start(token))
    await asyncio.gather(web_task, bot_task)

if __name__ == "__main__":
    asyncio.run(main())
