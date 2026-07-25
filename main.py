import os
import asyncio
from aiohttp import web
from discord.ext import commands
import discord

# Configuração básica do Servidor Web para o Render não derrubar o bot
async def handle(request):
    return web.Response(text="Bot está online!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # O Render usa a porta dinâmica da variável PORT ou 10000 por padrão
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Servidor web rodando na porta {port}")

# Configuração do Bot do Discord
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado com sucesso como {bot.user}!")
    try:
        await bot.load_extension("cogs.gunvan")
        print("Cog da Gun Van carregada!")

        await bot.load_extension("cogs.rockstar_news")
        print("Cog da Rockstar carregada!")

        GUILD_ID = discord.Object(id=1529337265019551879) 
        bot.tree.clear_commands(guild=GUILD_ID)
        bot.tree.copy_global_to(guild=GUILD_ID)
        synced = await bot.tree.sync(guild=GUILD_ID)
        print(f"Comandos sincronizados: {len(synced)}")
    except Exception as e:
        print(f"Erro ao carregar extensões: {e}")

@bot.command()
async def sync(ctx):
    try:
        bot.tree.copy_global_to(guild=ctx.guild)
        synced = await bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"✅ Sincronizados {len(synced)} comandos neste servidor!")
    except Exception as e:
        await ctx.send(f"❌ Erro ao sincronizar: {e}")

# Função Principal que inicia os dois serviços juntos sem conflito
async def main():
    # Inicia o servidor web primeiro para o Render aceitar o deploy na hora
    web_task = asyncio.create_task(start_web_server())
    
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("ERRO: DISCORD_TOKEN não configurado!")
        return

    # Inicia o bot do Discord em segundo plano
    bot_task = asyncio.create_task(bot.start(token))
    
    await asyncio.gather(web_task, bot_task)

if __name__ == "__main__":
    asyncio.run(main())
