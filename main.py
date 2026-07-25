import os
import asyncio
from aiohttp import web
from discord.ext import commands
import discord

# Servidor web obrigatório para o Render manter o bot ativo
async def handle(request):
    return web.Response(text="Bot da Gun Van e Rockstar online!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Servidor web rodando na porta {port}")

# Configuração do Bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}!")
    try:
        # Carrega a Cog da Gun Van
        await bot.load_extension("cogs.gunvan")
        print("Cog da Gun Van carregada com sucesso!")

        # Carrega a Cog de Notícias da Rockstar
        await bot.load_extension("cogs.rockstar_news")
        print("Cog da Rockstar carregada com sucesso!")

        # Sincroniza os comandos no seu servidor instantaneamente
        GUILD_ID = discord.Object(id=1529337265019551879) 
        bot.tree.clear_commands(guild=GUILD_ID)
        bot.tree.copy_global_to(guild=GUILD_ID)
        synced = await bot.tree.sync(guild=GUILD_ID)
        print(f"Comandos sincronizados com sucesso: {len(synced)}")
        
    except Exception as e:
        print(f"Erro ao carregar ou sincronizar: {e}")

async def main():
    web_task = asyncio.create_task(start_web_server())
    
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("ERRO: DISCORD_TOKEN não configurado nas variáveis de ambiente!")
        return

    bot_task = asyncio.create_task(bot.start(token))
    await asyncio.gather(web_task, bot_task)

if __name__ == "__main__":
    asyncio.run(main())
