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
        # if no meme specified get a random meme
        if meme_name == None:
            meme_name = random.choice([key for key in self.memedb.keys()])

        srv_id       = str(ctx.guild.id)
        image_dirs   = [global_image_dir, os.path.join(image_dir, srv_id)]
        meme_obj     = self.memedb[str(meme_name)]
        num_captions = len(meme_obj.captions)

        if len(args) == 0:
            msgs = []
            emotion_cog  = self.bot.get_cog('TextEmotion')
            for i in range(num_captions):
                emotion    = meme_obj.captions[i]["emotion"]
                subjective = meme_obj.captions[i]["subjective"]
                msgs += await emotion_cog.get_rand_message(
                        srv_id, emotion, subjective)
            meme_obj.create_meme(msgs, image_dirs)
        elif len(args) != num_captions:
            await ctx.send(f"Not enough arguments give, either give none or {len(meme_obj.captions)}")
            return
        else:
            meme_obj.create_meme(arg, image_dirs)
        print(f'sending meme: {meme_name}...')
        await ctx.channel.send(file=discord.File(temp_image_name))

    
    @meme.error
    async def meme_error(self, ctx, error):
        if isinstance(error, KeyError):
            await ctx.send(f"meme template specified does not exist or could not be found!")


    @commands.command(name="meme-rand-text")
    async def meme_rand(self, ctx, meme_name=None, *args):
        # if no meme specified get a random meme
        if meme_name == None:
            meme_name = random.choice([key for key in self.memedb.keys()])

        srv_id       = str(ctx.guild.id)
        image_dirs   = [global_image_dir, os.path.join(image_dir, srv_id)]
        meme_obj     = self.memedb[str(meme_name)]
        num_captions = len(meme_obj.captions)

        if len(args) == 0:
            markov_cog  = self.bot.get_cog('Markov')
            msgs = await markov_cog.get_chain(srv_id, num_captions)
            print(msgs)
            meme_obj.create_meme(msgs, image_dirs)
        elif len(args) != num_captions:
            await ctx.send(f"Not enough arguments give, either give none or {len(meme_obj.captions)}")
            return
        else:
            print("args!=0")
            meme_obj.create_meme(arg, image_dirs)
        print(f'sending meme: {meme_name}...')
        await ctx.channel.send(file=discord.File(temp_image_name))

    @meme_rand.error
    async def meme_rand_error(self, ctx, error):
        if isinstance(error, KeyError):
            await ctx.send(f"meme template specified does not exist or could not be found!")


    @commands.command(name="addimg")
    async def add_img(self, ctx, url):
        urllib.request.urlretrieve(url, temp_image_name)
        file_type = imghdr.what(temp_image_name)
        if file_type == None:
            await cxt.send("Invalid File Type")

        name   = uuid.uuid1()
        srv_id = str(ctx.guild.id)

        if not os.path.exists(f'{image_dir}/{srv_id}'):
            os.makedirs(f'{image_dir}/{srv_id}')

        image_destination = f"{image_dir}/{srv_id}/{str(name)}.{file_type}"

        print("adding image: " + str(image_destination))
        await ctx.send("adding image: " + str(image_destination))
        os.rename(temp_image_name, image_destination)
