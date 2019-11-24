import discord
from discord.ext import commands

import os
from os.path import isfile, join

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import random
from meme_templates import *
from dotenv import load_dotenv



# load environment variables (relavent ones are stored in .env)
load_dotenv()
token        = os.getenv('DISCORD_TOKEN')
template_dir = os.getenv('MEME_TEMPLATE_DIR')

# create bot object (subclass of client object)
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name="meme")
async def send_pic(ctx, *args):

    # get all the meme templates (images)
    #templates = 
    #    [f for f in os.listdir(template_dir) if isfile(join(template_dir, f))]

    text_box1 = ""
    text_box2 = ""

    if len(args) >= 1:
        text_box1 = args[0];
    if len(args) >= 2:
        text_box2 = args[1];

    two_buttons = meme_templates(
        "two-buttons", "two-buttons.jpg", 
        text_regions=[(62,84,230,170), (260,50,448,126)])

    two_buttons.create_meme(text_box1,text_box2)
    #rand = join(template_dir, random.choice(templates)) # choose a rand image

    print(f'sending meme...')
    await ctx.channel.send(file=discord.File('temp.jpg'))

bot.run(token)
