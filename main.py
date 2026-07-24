import asyncio
import logging
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

os.makedirs("logs", exist_ok=True)
logger = logging.getLogger("bot")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(filename="logs/bot.log", encoding="utf-8", mode="a")
file_handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


class GunVanBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)
        self.logger = logger

    async def setup_hook(self):
        await self.load_extension("cogs.gunvan")
        try:
            synced = await self.tree.sync()
            self.logger.info(f"Sincronizados {len(synced)} comandos de barra.")
        except Exception as e:
            self.logger.error(f"Erro ao sincronizar comandos: {e}")

    async def on_ready(self):
        self.logger.info(f"Bot conectado com sucesso como {self.user} (ID: {self.user.id})")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a Gun Van do GTA"))


async def main():
    if not TOKEN:
        logger.critical("Token do Discord não encontrado!")
        return

    bot = GunVanBot()
    async with bot:
        await bot.start(TOKEN)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot encerrado manualmente.")

