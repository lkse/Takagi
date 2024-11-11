import discord
from discord.ext import commands
import os
from .config import config

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='{config.DISCORD_PREFIX}', intents=intents)

async def init():
    from .logger import log
    log.info("[medium_spring_green blink]Bot Init[medium_spring_green blink]")
    # Load all cogs from the 'cogs' directory
    for filename in os.listdir('./app/cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'app.cogs.{filename[:-3]}')
    
    await bot.start(config.DISCORD_TOKEN)

async def shutdown():
    from .logger import log
    log.info("[red blink]Exiting Gracefully[red blink]")
    await bot.change_presence(status=discord.Status.offline, activity=None)
    await bot.close()
    
    