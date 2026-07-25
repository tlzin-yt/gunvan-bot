import os
import asyncio
from aiohttp import web
from discord.ext import commands
import discord

# Servidor web obrigatório para o Render
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

# Configuração do Bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado com sucesso como {bot.user}!")
    try:
        # Carrega a cog da Gun Van
        await bot.load_extension("cogs.gunvan")
        print("Cog da Gun Van carregada com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar a cog da Gun Van: {e}")

# Comando de sync 100% limpo e à prova de falhas
@bot.command(name="sync")
async def sync_command(ctx):
    try:
        # Sincroniza apenas os comandos da árvore atual sem tentar copiar nada global
        synced = await bot.tree.sync()
        await ctx.send(f"✅ Sincronizado com sucesso! {len(synced)} comandos atualizados.")
        print(f"Comandos sincronizados: {len(synced)}")
    except Exception as e:
        await ctx.send(f"❌ Erro ao sincronizar: {e}")
        print(f"Erro no sync: {e}")

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
