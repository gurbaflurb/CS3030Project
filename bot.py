import os
from os.path import isfile, join

import random
from dotenv import load_dotenv

import discord
from discord.ext import commands

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# load environment variables (relavent ones are stored in .env)
load_dotenv()
token        = os.getenv('DISCORD_TOKEN')
template_dir = os.getenv('MEME_TEMPLATE_DIR')

# create bot object (subclass of client object)
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name="mymeme")
async def send_pic(ctx, *args):

    # Defaults
    top_text = ""
    bottom_text = ""

    # get all the arguments
    if len(args) >= 1:
        top_text = args[0];
    if len(args) >= 2:
        bottom_text = args[1];

    # get all the meme templates (images)
    templates = [f for f in os.listdir(template_dir) 
            if isfile(join(template_dir, f))]
    rand = join(template_dir, random.choice(templates)) # choose a rand image

    
    img = Image.open(rand)
    width, height = img.size
    
    xpos        = int(width  * 0.00)
    bottom_ypos = int(height * 0.85)
    font_size   = int(height * 0.10) # about the right fnt size for image size

    meme = ImageDraw.Draw(img) # draw on image object

    fnt = ImageFont.truetype('fonts/comicsansms3.ttf', font_size)
    meme.multiline_text((xpos, 0), top_text, font=fnt, align="center")
    meme.multiline_text((xpos, bottom_ypos), bottom_text, font=fnt, align="center")

    img.save('temp.jpg')

    print(f'sending random picture: {rand}')
    await ctx.channel.send(file=discord.File('temp.jpg'))

bot.run(token)
