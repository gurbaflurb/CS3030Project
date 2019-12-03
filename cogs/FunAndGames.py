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

    @commands.command(name='echo')
    async def echo(self, ctx, *args):
	    await ctx.send(' '.join(args))


    @echo.error
    async def echo_error(self, ctx, error):
	    await ctx.send("You didn't give me anything to echo ಥ_ಥ")


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
    

    @commands.command(name='spongebob')
    async def spongeBobText(self, ctx, arg=None):
        if(arg == None):
            history = await ctx.history(limit=2).flatten()
            lastMsg = history[1].content
            if(lastMsg == '!spongebob'):
                await ctx.send("Can't find text")
        else:
            lastMsg = arg
        returnChar = ''
        for character in lastMsg:
            randValue = random.randint(0,1)
            if(randValue == 0):
                returnChar = returnChar + character.upper()
            else:
                returnChar = returnChar + character.lower()
        await ctx.send(returnChar)

    
