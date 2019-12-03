from discord.ext import commands
import discord
import os
import random
import shelve
from dotenv import load_dotenv

load_dotenv()

class History(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = shelve.open('history.db')

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
        print(returnHistory)
        await ctx.send("I got dat history, there's no hiding now W0mp")
        self.db['history'] = returnHistory

    @getHistory.error
    async def history_error(self, ctx, error):
        if isinstance(error, commands.ArgumentParsingError):
            await ctx.send("You didn't give me valid arguments ಥ_ಥ")
        else:
            await ctx.send(f"An  error has occured oof:\n !f{error}")


    async def get_random_messages(self, num: int):
        messages = [random.choice(self.db['history']) for i in range(num)]
        return tuple(messages)
