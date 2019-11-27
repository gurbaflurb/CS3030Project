from discord.ext import commands
import discord
import os
import random
from dotenv import load_dotenv

load_dotenv()
image_dir = os.getenv('IMAGE_DIR')

class FunAndGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="woaj")
    async def woaj(self, ctx):
        await ctx.channel.send(file=discord.File(f'{image_dir}/woaj.jpg'))


    @commands.command(name="rr")
    async def russian_roulete(self, ctx, *args):
        randnum = random.randint(0,5)
        print(ctx.author)

        if randnum == 0:
            await ctx.channel.send("🔫 ***BANG*** see ya " + ctx.author.mention)
            await ctx.guild.kick(ctx.author)
        else:
            await ctx.channel.send("*click*")
