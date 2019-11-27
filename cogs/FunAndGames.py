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
    
    @commands.command(name='history')
    async def getHistory(self, ctx, arg: int):
        history = await ctx.history(limit=arg).flatten()
        print(type(history.content))
        returnHistory = []
        for chatMsg in history:
            if('!history' in chatMsg.content or chatMsg.content == ''):
                num = num+1
                continue
            else:
                returnHistory.append(chatMsg.content)
        await ctx.send(returnHistory)

    @getHistory.error
    async def history_error(self, ctx, error):
        if isinstance(error, commands.ArgumentParsingError):
            await ctx.send("You didn't give me valid arguments ಥ_ಥ")
        else:
            await ctx.send("An error has occured oof")
    
    '''
    @commands.command(name='spongebob')
    async def spongeBobText(self, ctx, arg):
        if(message.content == '!spongebob'):
            history = await message.channel.history(limit=100).flatten()
            for word in history:
                if(word.content.startswith('!spongebob')):
                    continue
                else:
                    tempText = word.content
                    break
            returnChar = ''
            for character in tempText:
                randValue = random.randint(0,1)
                if(randValue == 0):
                    returnChar = returnChar + character.upper()
                else:
                    returnChar = returnChar+character
            return returnChar
    '''