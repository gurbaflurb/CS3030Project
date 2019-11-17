import os
import random
from dotenv import load_dotenv

import discord
from discord.ext import commands

# load environment variables (relavent ones are stored in .env)
load_dotenv()
token     = os.getenv('DISCORD_TOKEN')
templates = os.getenv('MEME_TEMPLATE_DIR')

# create bot object (subclass of client object)
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name="pic")
async def send_pic(ctx):
    await ctx.channel.send(file=discord.File(f'{PIC_DIR}/vapor.jpg'))

bot.run(token)
