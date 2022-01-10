import discord
from discord.commands import slash_command, Option
from discord.commands.context import AutocompleteContext
from discord.ext import commands

import json
import aiohttp
import io
import re
from colorthief import ColorThief
from utils.async_cacher import async_cacher

@async_cacher()
async def get_apps_autocompleter():
    res_apps = []
    async with aiohttp.ClientSession() as session:
        async with session.get('https://jailbreaks.app/json/apps.json') as resp:
            if resp.status == 200:
                data = await resp.text()
                apps = json.loads(data)

                # try to find an app with the name given in command
                for d in apps:
                    name = re.sub(r'\((.*?)\)', '', d.get('name'))
                    # get rid of '[ and ']'
                    name = name.replace('[', '')
                    name = name.replace(']', '')
                    name = name.strip()
                    if name not in res_apps:
                        res_apps.append(name)

    return res_apps

async def apps_autocomplete(ctx: AutocompleteContext):
    apps = await get_apps_autocompleter()
    apps.sort()
    return [app for app in apps if app.lower().startswith(ctx.value.lower())][:25]

async def get_stats(query):
    res_stats = []
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.jailbreaks.app/stats/all') as resp:
            if resp.status == 200:
                data = await resp.text()
                stats = json.loads(data).get('stats')
                res_stats = stats.get(query)

    return res_stats

@async_cacher()
async def get_apps():
    res_apps = []
    async with aiohttp.ClientSession() as session:
        async with session.get('https://jailbreaks.app/json/apps.json') as resp:
            if resp.status == 200:
                data = await resp.text()
                res_apps = json.loads(data)
                
    return res_apps

async def iterate_apps(query) -> dict:
    apps = await get_apps()
    for possibleApp in apps:
        if possibleApp.get('name').lower() == query.lower():
            return possibleApp

class App(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description='Get info about an app.')
    async def app(self, ctx: discord.ApplicationContext, name: Option(str, description='Name of the app', autocomplete=apps_autocomplete, required=True)) -> None:
        app_ = await iterate_apps(query=name)
        if app_ == None:
            await ctx.respond("That app isn't on Jailbreaks.app.", ephemeral=True)
            return
        stats = await get_stats(query=app_.get('name'))
        mainDLLink = f"https://api.jailbreaks.app/install/{name.replace(' ', '')}"
        allVersions = f"[Latest ({app_.get('version')})]({mainDLLink})"
        if len(app_.get('other_versions')) != 0:
            for version in app_.get('other_versions'):
                allVersions += f"\n[{version}]({mainDLLink}/{version})"
        embed = discord.Embed(title=app_.get('name'), color=int(app_.get('color').replace('#', ''), 16), url=mainDLLink, description=app_.get('short-description'))
        embed.set_thumbnail(url=f"https://jailbreaks.app/{app_.get('icon')}")
        embed.add_field(name=f"Download Link{'' if len(app_.get('other_versions')) == 0 else 's'}", value=allVersions, inline=True)
        embed.add_field(name='Developer', value=f"{('[' + app.get('dev') + '](https://twitter.com/' + app_.get('dev') + ')') if app_.get('dev').startswith('@') else app_.get('dev')}", inline=True)
        embed.add_field(name='Downloads', value='{:,}'.format(int(stats)))
        embed.set_footer(text='Jailbreaks.app | Made by Jaidan', icon_url='https://avatars.githubusercontent.com/u/37126748')
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(App(bot))
