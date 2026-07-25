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

@bot.event
async def on_ready():
    print(f"CONECTADO COM SUCESSO COMO: {bot.user}")
    try:
        await bot.load_extension("cogs.gunvan")
        print("Cog Gunvan carregada!")
        
        await bot.load_extension("cogs.rockstar_news")
        print("Cog Rockstar carregada!")

        GUILD_ID = discord.Object(id=1529337265019551879)
        bot.tree.clear_commands(guild=GUILD_ID)
        bot.tree.copy_global_to(guild=GUILD_ID)
        synced = await bot.tree.sync(guild=GUILD_ID)
        print(f"COMANDOS SINCRONIZADOS: {len(synced)}")
    except Exception as e:
        print(f"ERRO CRÍTICO NO ON_READY: {e}")

async def handle(request):
    return web.Response(text="Bot online!")

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
    web_task = asyncio.create_task(start_web_server())
    token = os.getenv("DISCORD_TOKEN")
    if token:
        bot_task = asyncio.create_task(bot.start(token))
        await asyncio.gather(web_task, bot_task)
    else:
        print("ERRO: DISCORD_TOKEN não encontrado!")

if __name__ == "__main__":
    asyncio.run(main())
