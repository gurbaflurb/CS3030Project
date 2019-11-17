import os
from os.path import isfile, join

import random
from dotenv import load_dotenv

import discord
from discord.ext import commands

# load environment variables (relavent ones are stored in .env)
load_dotenv()
token        = os.getenv('DISCORD_TOKEN')
template_dir = os.getenv('MEME_TEMPLATE_DIR')

# create bot object (subclass of client object)
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name="pic")
async def send_pic(ctx):

    pics = [f for f in os.listdir(template_dir) 
            if isfile(join(template_dir, f))]

    rand_pic = join(template_dir, random.choice(pics))

    print(f'sending random picture: {rand_pic}')
    await ctx.channel.send(file=discord.File(rand_pic))

bot.run(token)
