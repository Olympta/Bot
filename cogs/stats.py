import discord
from discord.commands import slash_command, Option
from discord.commands.context import AutocompleteContext
from discord.ext import commands
from discord.utils import format_dt

import psutil
import os
import platform
from datetime import datetime
from math import floor

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now()
        
    @slash_command(description='Get info about the bot.')
    async def stats(self, ctx: discord.ApplicationContext) -> None:
        process = psutil.Process(os.getpid())
        members = 0
        
        for guild in self.bot.guilds:
            members += guild.member_count
        
        embed = discord.Embed(title=f"{self.bot.user.name} Statistics", color=discord.Color.red())
        embed.description = f"Serving {members} members in {len(self.bot.guilds)} guilds."
        embed.set_thumbnail(url=self.bot.user.display_avatar)
        embed.add_field(name='Bot Started', value=format_dt(self.start_time, style='R'))
        embed.add_field(name='CPU Usage', value=f"{psutil.cpu_percent()}%")
        embed.add_field(name='Memory Usage', value=f"{floor(process.memory_info().rss/1000/1000)} MB")
        embed.add_field(name='Python Version', value=platform.python_version())
        embed.set_footer(text='Jailbreaks.app | Made by Jaidan', icon_url='https://avatars.githubusercontent.com/u/37126748')

        await ctx.respond(embed=embed, ephemeral=True)
    
    @slash_command(description="Test bot and Discord API latency.")
    async def ping(self, ctx: discord.ApplicationContext) -> None:
        embed = discord.Embed(title="Pong!", color=discord.Color.green())
        embed.set_thumbnail(url=self.bot.user.display_avatar)
        embed.description = "Testing latency..."

        time_started = datetime.utcnow()
        await ctx.respond(embed=embed, ephemeral=True)

        ping = floor((datetime.utcnow() - time_started).total_seconds() * 1000)
        if ping >= 500 and ping <= 800:
            embed.color = discord.Color.yellow()
        elif ping >= 800:
            embed.color = discord.Color.red()
        embed.description = ""
        embed.add_field(name="Message Latency", value=f"```{ping} ms```")
        embed.add_field(name="API Latency", value=f"```{floor(self.bot.latency*1000)} ms```")
        await ctx.edit(embed=embed)
        
def setup(bot):
    bot.add_cog(Info(bot))
