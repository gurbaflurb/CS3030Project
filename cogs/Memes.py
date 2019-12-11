from discord.ext import commands
import discord
import uuid
import imghdr
import shelve
import os
import random
import urllib.request
from meme_templates import MemeTemplates
from dotenv import load_dotenv

load_dotenv()
template_dir     = os.getenv('MEME_TEMPLATE_DIR')
image_dir        = os.getenv('IMAGE_DIR')
global_image_dir = os.getenv('GLOBAL_IMAGE_DIR')
temp_image_name  = os.getenv('TEMP_IMAGE')

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.memedb = shelve.open('memes.db')

    @commands.command(name="meme")
    async def meme(self, ctx, meme_name=None, *args):
        if meme_name == None:
            names = [key for key in self.memedb.keys()]
            meme_name = random.choice(names)

        meme_obj = self.memedb[str(meme_name)]
        num_regs = meme_obj.num_text_regs
        srv_id   = str(ctx.guild.id)

        assert len(args) == 0 or len(args) == num_regs,\
                "incorrect number of arguments"

        image_dirs = [global_image_dir, os.path.join(image_dir, srv_id)]

        if len(args) == 0:
            hist_cog = self.bot.get_cog('History')
            rand = await hist_cog.get_random_messages(ctx, num_regs)
            meme_obj.create_meme(rand, image_dirs)
        else:
            meme_obj.create_meme(arg, image_dirs)
        print(f'sending meme: {meme_name}...')
        await ctx.channel.send(file=discord.File(temp_image_name))
    
    @meme.error
    async def meme_error(self, ctx, error):
        if isinstance(error, KeyError):
            await ctx.channel.send(f"meme template specified does not exist or could not be found!")
        else:
            await ctx.send(f"An  error has occured oof:\n !f{error}")


    @commands.command(name="meme-rand-text")
    async def meme_rand(self, ctx, meme_name=None, *args):

        if meme_name == None:
            names = [key for key in self.memedb.keys()]
            meme_name = random.choice(names)

        meme_obj = self.memedb[str(meme_name)]
        num_regs = meme_obj.num_text_regs
        srv_id   = str(ctx.guild.id)

        assert len(args) == 0 or len(args) == num_regs,\
                "incorrect number of arguments"

        image_dirs = [global_image_dir, os.path.join(image_dir, srv_id)]

        if len(args) == 0:
            mark_cog = self.bot.get_cog('Markov')
            rand = await mark_cog.get_chain(srv_id, num_regs)
            meme_obj.create_meme(rand, image_dirs)
        else:
            meme_obj.create_meme(args, image_dirs)
        print(f'sending meme: {meme_name}...')
        await ctx.channel.send(file=discord.File(temp_image_name))

    @meme_rand.error
    async def meme_rand_error(self, ctx, error):
        await ctx.send(f"Looks like an error occured:\n f{error}")


    @commands.command(name="addimg")
    async def add_img(self, ctx, url):

        try: # Change how the file type is detected, since right now it looks like a text file could be uploaded(ie. anything but a None type will work)
            urllib.request.urlretrieve(url, temp_image_name)
            file_type = imghdr.what(temp_image_name)
            assert file_type != None, "file is Not image type"

            name = uuid.uuid1()
            srv_id = str(ctx.guild.id)

            if not os.path.exists(f'{image_dir}/{srv_id}'):
                os.makedirs(f'{image_dir}/{srv_id}')

            name = f"{image_dir}/{srv_id}/{str(name)}.{file_type}"

            print("adding image: " + str(name))
            await ctx.channel.send("adding image: " + str(name))
            os.rename("temp.jpg", name)
        except AssertionError:
            await ctx.channel.send("Incorrect file type")

    @add_img.error
    async def add_img_error(self, ctx, error):
        await ctx.channel.send(f"Oh noes, and error has occured:\n f{error}")
