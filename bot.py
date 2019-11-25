import discord
from discord.ext import commands

import os
from os.path import isfile

import urllib.request
import uuid
import imghdr

from meme_templates import *
from dotenv import load_dotenv


# load environment variables (relavent ones are stored in .env)
load_dotenv()
token           = os.getenv('DISCORD_TOKEN')
template_dir    = os.getenv('MEME_TEMPLATE_DIR')
image_dir       = os.getenv('IMAGE_DIR')
temp_image_name = os.getenv('TEMP_IMAGE')

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
    await ctx.channel.send(file=discord.File(temp_image_name))


@bot.command(name="drake")
async def drake(ctx, *args):
    drake = meme_templates(
        "drake", "drake.jpg", 
        image_regions=[(601,0,1197,591), (601,592,1197,1197)])

    drake.create_meme()
    print(f'sending drake...')
    await ctx.channel.send(file=discord.File(temp_image_name))


@bot.command(name="rr")
async def russian_roulete(ctx, *args):
    randnum = random.randint(0,5)
    print(ctx.author)

    if randnum == 0:
        await ctx.channel.send("🔫 ***BANG*** see ya " + ctx.author.mention)
        await ctx.guild.kick(ctx.author)
    else:
        await ctx.channel.send("*click*")


@bot.command(name="addimg")
async def add_img(ctx, url):

    try:
        urllib.request.urlretrieve(url, "temp.jpg")
        file_type = imghdr.what("temp.jpg")
        assert file_type == "None", "file is Not image type"

        name = uuid.uuid1()
        name = f"{image_dir}/{str(name)}.{file_type}"

        print("adding image: " + str(name))
        os.rename("temp.jpg", name)
    except AssertionError:
        await ctx.channel.send("Incorrect file type")


@bot.command(name="woaj")
async def woaj(ctx):
    await ctx.channel.send(file=discord.File(f'{image_dir}/woaj.jpg'))

bot.run(token)

