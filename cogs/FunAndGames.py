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

    @commands.command(name='reload', hidden=True)
    async def _reload(self, ctx, *, arg):
        try:
            self.bot.reload_extension(arg)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send('Reloaded {}'.format(arg))

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
    
    @commands.command(name='history')
    async def getHistory(self, ctx, arg: int):
        history = await ctx.history(limit=150).flatten()
        del history[0] # ignore message that called this command
        returnHistory = []

        for chatMsg in range(0, arg+1):
            if (history[chatMsg].content == '' 
                    or history[chatMsg].content[0] == '!'
                    or history[chatMsg].author.bot):
                continue
            else:
                returnHistory.append(history[chatMsg].content)
        #await ctx.send(returnHistory)
        print(ctx.send(returnHistory))
        return returnHistory

    @getHistory.error
    async def history_error(self, ctx, error):
        if isinstance(error, commands.ArgumentParsingError):
            await ctx.send("You didn't give me valid arguments ಥ_ಥ")
        else:
            await ctx.send(f"An  error has occured oof:\n !f{error}")
    
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

    
