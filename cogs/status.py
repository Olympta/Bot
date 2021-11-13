import discord
from discord.commands import slash_command
from discord.ext import commands

from utils.fetch_status import fetch_status

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Gets status of Jailbreaks.app's certificate.")
    async def status(self, ctx: discord.ApplicationContext) -> None:
        status = (await fetch_status()).get('status')
        await self.bot.change_presence(activity=discord.Game(name="{} | https://jailbreaks.app".format(status)))
        embed = discord.Embed(title='Jailbreaks.app Status')
        embed.set_thumbnail(url='https://jailbreaks.app/img/Jailbreaks.png')
        embed.set_footer(text="Jailbreaks.app | Made by Jaidan", icon_url="https://avatars.githubusercontent.com/u/37126748")
        if status == "Signed":
            embed.description = 'Jailbreaks.app is currently **signed.** This means that all of our apps are installable and usable. If you can’t install / open an app, you are likely blacklisted from using the current certificate.'
            embed.color = discord.Color.green()
        else:
            embed.description = 'Jailbreaks.app is currently **revoked.** This means that our apps are not installable or usable as of now.'
            embed.color = discord.Color.red()
        await ctx.respond(embed=embed)
        
def setup(bot):
    bot.add_cog(Status(bot))
