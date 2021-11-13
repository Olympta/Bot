import discord

from utils.fetch_status import fetch_status
from utils.logging import logger
from dotenv import load_dotenv
import os

logger.info('Loading environment...')
load_dotenv()

logger.info('Initializing client...')
cogs = [
    'cogs.status',
    'cogs.app',
    'cogs.stats'
]
bot = discord.Bot(status=discord.Status.dnd)
initial_extensions = []
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.presences = True
mentions = discord.AllowedMentions(everyone=False, users=True, roles=False)

@bot.event
async def on_ready():
    print('''                                                                                         
   88            88 88 88                                           88                   
   ""            "" 88 88                                           88                   
                    88 88                                           88                   
   88 ,adPPYYba, 88 88 88,dPPYba,  8b,dPPYba,  ,adPPYba, ,adPPYYba, 88   ,d8  ,adPPYba,  
   88 ""     `Y8 88 88 88P'    "8a 88P'   "Y8 a8P_____88 ""     `Y8 88 ,a8"   I8[    ""  
   88 ,adPPPPP88 88 88 88       d8 88         8PP""""""" ,adPPPPP88 8888[      `"Y8ba,   
   88 88,    ,88 88 88 88b,   ,a8" 88         "8b,   ,aa 88,    ,88 88`"Yba,  aa    ]8I  
   88 `"8bbdP"Y8 88 88 8Y"Ybbd8"'  88          `"Ybbd8"' `"8bbdP"Y8 88   `Y8a `"YbbdP"'  
  ,88                                                                                    
888P"                                                                     
    ''')
    await bot.change_presence(activity=discord.Game(name="{} | https://jailbreaks.app".format((await fetch_status()).get('status'))))
    logger.info("Successfully logged in as {}".format(bot.user))
    
if __name__ == '__main__':
    for cog in cogs:
        logger.info("Loading '{}'".format(cog))
        bot.load_extension(cog)
        
bot.run(os.environ.get('BOT_TOKEN'), reconnect=True)