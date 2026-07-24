from datetime import datetime
import os
import discord
from discord import app_commands
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from utils.scraper import fetch_gun_van_data


class GunVanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler(timezone="America/Sao_Paulo")
        self.channel_id = int(os.getenv("CHANNEL_ID", 0))

        self.scheduler.add_job(self.daily_gun_van_task, CronTrigger(hour=6, minute=0))
        self.scheduler.start()

    def cog_unload(self):
        self.scheduler.shutdown()

    async def daily_gun_van_task(self):
        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            self.bot.logger.error(f"Canal com ID {self.channel_id} não foi encontrado.")
            return

        data = fetch_gun_van_data()
        if not data["success"]:
            self.bot.logger.error(f"Falha na tarefa automática: {data.get('error')}")
            return

        embed = discord.Embed(
            title="🗺️ Localização da Gun Van",
            color=discord.Color.red(),
            timestamp=datetime.now(),
        )
        embed.add_field(name="📍 Localização", value=data["location"], inline=False)
        embed.add_field(name="📅 Data", value=datetime.now().strftime("%d/%m/%Y"), inline=True)
        embed.set_image(url=data["image_url"])
        embed.add_field(name="🔗 Link", value=f"[Acessar GTAMap]({data['link']})", inline=False)
        embed.set_footer(text="Atualização automática diária")

        await channel.send(content="🚨 **Atualização diária da Gun Van disponível!**", embed=embed)
        self.bot.logger.info("Mensagem automática enviada com sucesso.")

    @app_commands.command(name="gunvan", description="Mostra a localização atual da Gun Van.")
    async def gunvan(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        data = fetch_gun_van_data()
        if not data["success"]:
            await interaction.followup.send("❌ Ocorreu um erro ao buscar os dados.", ephemeral=True)
            return

        embed = discord.Embed(
            title="🗺️ Localização da Gun Van",
            color=discord.Color.red(),
            timestamp=datetime.now(),
        )
        embed.add_field(name="📍 Localização", value=data["location"], inline=False)
        embed.add_field(name="📅 Data", value=datetime.now().strftime("%d/%m/%Y"), inline=True)
        embed.set_image(url=data["image_url"])
        embed.add_field(name="🔗 Link", value=f"[Acessar GTAMap]({data['link']})", inline=False)
        embed.set_footer(text="Solicitado via comando /gunvan")

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="ping", description="Mostra a latência atual do bot.")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"🏓 Pong! A latência atual é de **{latency}ms**.", ephemeral=True)

    @app_commands.command(name="ajuda", description="Lista todos os comandos disponíveis.")
    async def ajuda(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 Central de Ajuda - Gun Van Bot",
            description="Lista de comandos interativos disponíveis:",
            color=discord.Color.blue(),
        )
        embed.add_field(name="/gunvan", value="Exibe a localização atual e o mapa.", inline=False)
        embed.add_field(name="/ping", value="Verifica a latência do bot.", inline=False)
        embed.add_field(name="/ajuda", value="Mostra esta mensagem de ajuda.", inline=False)
        embed.set_footer(text="Desenvolvido com discord.py 2.x")

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(GunVanCog(bot))

