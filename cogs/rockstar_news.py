import discord
from discord.ext import commands
from discord import app_commands

class RockstarNews(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="rockstar", description="Mostra as últimas notícias da Rockstar")
    async def rockstar(self, interaction: discord.Interaction):
        await interaction.response.send_message("📰 Buscando as últimas notícias da Rockstar...", ephemeral=False)
        # Coloque aqui a lógica de busca que você já tinha no seu utilitário da Rockstar

async def setup(bot):
    await bot.add_cog(RockstarNews(bot))

