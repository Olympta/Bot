import discord
from discord.commands import slash_command
from discord.ext import commands

from utils.fetch_status import fetch_status

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Gets status of Jailbreaks.app's certificate.")
    async def status(self, ctx: discord.ApplicationContext) -> None:
        status = (await fetch_status()).get("status")
        embed = discord.Embed(title="Jailbreaks.app Status")
        embed.set_thumbnail(url="https://jailbreaks.app/img/Jailbreaks.png")
        embed.set_footer(text="SignedBot | Made by Jaidan", icon_url="https://avatars.githubusercontent.com/u/37126748")
        if status == "Signed":
            embed.add_field(name="Status", value="Signed!")
            embed.color = discord.Color.green()
        else:
            embed.add_field(name="Status", value="Revoked.")
            embed.color = discord.Color.red()
        await ctx.respond(embed=embed)
        
def setup(bot):
    bot.add_cog(Status(bot))
