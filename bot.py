import discord
from discord.ext import commands

import os
from os.path import isfile

import urllib.request
import uuid
import imghdr

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from meme_templates import *
from dotenv import load_dotenv



# load environment variables (relavent ones are stored in .env)
load_dotenv()
token        = os.getenv('DISCORD_TOKEN')
template_dir = os.getenv('MEME_TEMPLATE_DIR')

# create bot object (subclass of client object)
bot = commands.Bot(command_prefix='!')
client = discord.Client()


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name="meme")
async def send_pic(ctx, *args):
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

    print(f'sending meme...')
    await ctx.channel.send(file=discord.File('temp.jpg'))


@bot.command(name="drake")
async def drake(ctx, *args):
    drake = meme_templates(
        "drake", "drake.jpg", 
        image_regions=[(601,0,1197,591), (601,592,1197,1197)])

    drake.create_meme()
    print(f'sending drake...')
    await ctx.channel.send(file=discord.File('temp.jpg'))


@bot.command(name="rr")
async def russian_roulete(ctx, *args):
    randnum = random.randint(0,5)
    print(ctx.author)

    if ctx.author.name == "Hayaikawa Blacky Uzi | NW":
        await ctx.channel.send("🔫 ***BANG*** see ya furry" + ctx.author.mention)
        await ctx.guild.kick(ctx.author)
    elif randnum == 0:
        await ctx.channel.send("🔫 ***BANG*** see ya " + ctx.author.mention)
        await ctx.guild.kick(ctx.author)
    else:
        await ctx.channel.send("*click*")


@bot.command(name="addimg")
async def add_img(ctx, url):

    urllib.request.urlretrieve(url, "temp.jpg")
    file_type = imghdr.what("temp.jpg")

    name = uuid.uuid1()
    name = "images/" + str(name) + f".{file_type}"


    if file_type != None:
        print("adding image: " + str(name))
        os.rename("temp.jpg", name)
    else:
        await ctx.channel.send("Incorrect file type")
        os.remove(name)


@bot.command(name="woaj")
async def woaj(ctx):
    await ctx.channel.send(file=discord.File('images/woaj.jpg'))

bot.run(token)

