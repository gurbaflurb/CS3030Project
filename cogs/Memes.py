from discord.ext import commands
import discord
import uuid
import imghdr
import shelve
import os
import urllib.request
from meme_templates import MemeTemplates
from dotenv import load_dotenv

load_dotenv()
template_dir    = os.getenv('MEME_TEMPLATE_DIR')
image_dir       = os.getenv('IMAGE_DIR')
temp_image_name = os.getenv('TEMP_IMAGE')

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.memedb = shelve.open('memes.db')

    @commands.command(name="meme")
    async def meme(self, ctx, meme_name="drake", *args):

        try:
            meme_obj = self.memedb[meme_name]
            meme_obj.create_meme(args)
            print(f'sending meme: {meme_name}...')
            await ctx.channel.send(file=discord.File(temp_image_name))
        except KeyError:
            await ctx.channel.send(f"meme \"{meme_name}\" does not exist")



    @commands.command(name="addimg")
    async def add_img(self, ctx, url):

        try:
            urllib.request.urlretrieve(url, temp_image_name)
            file_type = imghdr.what(temp_image_name)
            assert file_type != None, "file is Not image type"

            name = uuid.uuid1()
            name = f"{image_dir}/{str(name)}.{file_type}"

            print("adding image: " + str(name))
            await ctx.channel.send("adding image: " + str(name))
            os.rename("temp.jpg", name)
        except AssertionError:
            await ctx.channel.send("Incorrect file type")
