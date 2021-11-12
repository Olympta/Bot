import discord

from utils.logging import logger
from dotenv import load_dotenv
import os

logger.info("Loading environment...")
load_dotenv()

logger.info("Initializing client...")
cogs = [
    "cogs.status",
    "cogs.app"
]
bot = discord.Bot()
initial_extensions = []
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.presences = True
mentions = discord.AllowedMentions(everyone=False, users=True, roles=False)

@bot.event
async def on_ready():
    logger.info("Successfully logged in as {}".format(bot.user))
    
if __name__ == "__main__":
    for cog in cogs:
        logger.info("Loading '{}'".format(cog))
        bot.load_extension(cog)

bot.run(os.environ.get("BOT_TOKEN"), reconnect=True)