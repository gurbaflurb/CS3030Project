from discord.ext import commands
import discord
import os
import random
from dotenv import load_dotenv

load_dotenv()
image_dir = os.getenv('IMAGE_DIR')
global_image_dir = os.getenv('GLOBAL_IMAGE_DIR')

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
        await ctx.channel.send(file=discord.File(f'{global_image_dir}/woaj.jpg'))

    @woaj.error
    async def woaj_error(self, ctx, error):
        await ctx.channel.send(f"Woah, looks like an error occured f{error}")


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
        
    @spongeBobText.error
    async def spongeBobText_error(self, ctx, error):
        await ctx.channel.send(f"An error has occured in Bikini Bottom!\n f{error}")

    
    @commands.command(name='uwu')
    async def uwu(self, ctx, arg=None):
        if(arg == None):
            history = await ctx.history(limit=2).flatten()
            lastMsg = history[1].content
            uwuMsg = await self.makeUwUText(lastMsg)
        else:
            uwuMsg = await self.makeUwUText(arg)
        await ctx.send(uwuMsg)
            
    @uwu.error
    async def uwu_error(self, ctx, error):
        await ctx.send(f"OwO Oh Noes, Wooks wike an ewwow occuwed. Pwease dwon't hwate mwe .·´¯`(>▂<)´¯`·.\n f{error}")
        

    async def makeUwUText(self, lastMsg):
        uwuMsg = ''
        for letter in lastMsg:
            num = random.randint(0,11)
            if(letter.lower() == 'r' or letter.lower() == 'l'):
                uwuMsg = uwuMsg+'w'
            elif(letter is 'm' or letter is 'M'):
                uwuMsg = uwuMsg+letter+'w'
            elif(letter is ' '):
                if(num is 0):
                    uwuMsg = uwuMsg + " X3 "
                elif(num is 1):
                    uwuMsg = uwuMsg + " \*nuzzles\* "
                elif(num is 2):
                    uwuMsg = uwuMsg + " UwU "
                elif(num > 2):
                    uwuMsg = uwuMsg + " "
            else:
                uwuMsg = uwuMsg+letter
        return uwuMsg
