import discord
from discord.ext import commands, tasks
from discord import app_commands
from utils.rockstar_scraper import fetch_latest_rockstar_news

class RockstarNews(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_news_title = None
        self.check_news_loop.start()

    def cog_unload(self):
        self.check_news_loop.cancel()

    @tasks.loop(hours=1.0)
    async def check_news_loop(self):
        await self.bot.wait_until_ready()
        
        CHANNEL_ID = 1529481189730160711
        channel = self.bot.get_channel(CHANNEL_ID)
        if not channel:
            return

        news = fetch_latest_rockstar_news()
        if news["success"]:
            if news["title"] != self.last_news_title:
                self.last_news_title = news["title"]
                
                embed = discord.Embed(
                    title="🚨 NOVA NOTÍCIA DA ROCKSTAR GAMES",
                    description=f"**[{news['title']}]({news['link']})**",
                    color=discord.Color.gold()
                )
                embed.add_field(name="📅 Publicação", value=news["date"], inline=False)
                embed.set_image(url=news["image_url"])
                embed.set_footer(text="Complexo Zero11 • Atualizações Automáticas")
                
                await channel.send(embed=embed)

    @app_commands.command(name="rockstar", description="Mostra a última notícia oficial lançada pela Rockstar Games")
    async def rockstar_command(self, interaction: discord.Interaction):
        # Adia a resposta imediatamente para o Discord não dar timeout
        await interaction.response.defer(thinking=True)
        
        # Faz a busca da notícia de forma segura
        news = fetch_latest_rockstar_news()
        
        if not news["success"]:
            await interaction.followup.send("❌ Não foi possível carregar as notícias da Rockstar no momento.", ephemeral=True)
            return

        embed = discord.Embed(
            title="📰 Última Notícia da Rockstar Games",
            description=f"**[{news['title']}]({news['link']})**",
            color=discord.Color.red()
        )
        embed.add_field(name="📅 Publicação", value=news["date"], inline=False)
        embed.set_image(url=news["image_url"])
        embed.set_footer(text="Complexo Zero11")
        
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(RockstarNews(bot))
