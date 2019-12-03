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
        history = await ctx.history(limit=None, oldest_first=True).flatten()
        del history[0] # ignore message that called this command

        server  = str(ctx.guild.id)
        channel = str(ctx.channel.id)

        filtered = filter_messages(history)

        self.db[server] = {}
        self.db[server][channel] = filtered
        await ctx.send("I got dat history!")

    @getHistory.error
    async def history_error(self, ctx, error):
        if isinstance(error, commands.ArgumentParsingError):
            await ctx.send("You didn't give me valid arguments ಥ_ಥ")
        else:
            await ctx.send(f"An  error has occured oof:\n !f{error}")


    async def filter_messages(self, messages: list):
        filtered = []

        for chat_msg in messages:
            if (chat_msg.content == '' 
                    or chat_msg.content[0] == '!'
                    or chat_msg.author.bot):
                continue
            else:
                filtered.append(history[chatMsg].content)
        return filtered


    async def get_random_messages(self, num: int):
        messages = [random.choice(self.db['history']) for i in range(num)]
        return tuple(messages)
