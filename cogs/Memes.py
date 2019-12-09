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
template_dir    = os.getenv('MEME_TEMPLATE_DIR')
image_dir       = os.getenv('IMAGE_DIR')
temp_image_name = os.getenv('TEMP_IMAGE')

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.memedb = shelve.open('memes.db')

    @commands.command(name="meme-quote")
    async def meme_quote(self, ctx, meme_name="drake", *args):
        meme_obj = self.memedb[str(meme_name)]
        num_regs = meme_obj.num_text_regs

        assert len(args) == 0 or len(args) == num_regs,\
                "incorrect number of arguments"

        if len(args) == 0:
            hist_cog = self.bot.get_cog('History')
            rand = await hist_cog.get_random_messages(ctx, num_regs)
            meme_obj.create_meme(rand)
        else:
            meme_obj.create_meme(args)
        print(f'sending meme: {meme_name}...')
        await ctx.channel.send(file=discord.File(temp_image_name))

    @commands.command(name="meme")
    async def meme(self, ctx, meme_name="drake", *args):
        meme_obj = self.memedb[str(meme_name)]
        num_regs = meme_obj.num_text_regs
        srv_id   = str(ctx.guild.id)

        assert len(args) == 0 or len(args) == num_regs,\
                "incorrect number of arguments"

        if len(args) == 0:
            mark_cog = self.bot.get_cog('Markov')
            rand = await mark_cog.get_chain(srv_id, num_regs)
            meme_obj.create_meme(rand)
        else:
            meme_obj.create_meme(args)
        print(f'sending meme: {meme_name}...')
        await ctx.channel.send(file=discord.File(temp_image_name))

    @meme_quote.error
    async def meme_error(self, ctx, error):
        if isinstance(error, KeyError):
            await ctx.channel.send(f"meme \"{meme_name}\" does not exist")
        else:
            await ctx.send(f"An  error has occured oof:\n !f{error}")


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
