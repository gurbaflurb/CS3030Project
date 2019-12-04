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

    @commands.command(name='list-hist')
    @commands.has_any_role('mod', 'admin', '@mod')
    async def listHistory(self, ctx):
        for key in self.db.keys():
            server_name = self.bot.get_guild(id=int(key)).name
            print(f"{server_name}: {key}")
            for channel in self.db[key]:
                channel_name = self.bot.get_channel(id=int(channel)).name
                print(f"\t{channel_name}: {channel}")


    @commands.command(name='del-hist')
    @commands.has_any_role('mod', 'admin', '@mod')
    async def delHistory(self, ctx):
        for key in self.db.keys():
            del self.db[key]


    @commands.command(name='add-hist')
    @commands.has_any_role('mod', 'admin', '@mod')
    async def getHistory(self, ctx):
        print(f"Grabbing messages from {ctx.channel.name} this could take a while...")
        await ctx.send(f"Grabbing messages from {ctx.channel.name} this could take a while...")

        history = await ctx.history(limit=None, oldest_first=True).flatten()
        del history[0] # ignore message that called this command

        server  = str(ctx.guild.id)
        channel = str(ctx.channel.id)
        filtered = await self.filter_messages(history)

        
        if server not in self.db:
            self.db[server] = {}
        srv_dict = self.db[server]
        srv_dict[channel] = filtered
        self.db[server] = srv_dict

        print(f"Grabbed {len(filtered)} messages from {ctx.channel.name}")
        await ctx.send(f"Grabbed {len(filtered)} messages from {ctx.channel.name}")

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
                filtered.append(chat_msg.content)
        return filtered


    async def get_random_messages(self, ctx, num: int):
        server   = str(ctx.guild.id)
        channel  = str(ctx.channel.id)
        messages = self.db[server][channel]
        
        rand_msgs = [random.choice(messages) for i in range(num)]
        return tuple(rand_msgs)
