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

    @commands.command(name='list-all')
    @commands.has_any_role('mod', '@mod')
    async def listHistory(self, ctx):
        for key in self.db.keys():
            server_name = self.bot.get_guild(id=int(key)).name
            print(f"{server_name}: {key}")
            for channel in self.db[key]:
                channel_name = self.bot.get_channel(id=int(channel)).name
                print(f"\t{channel_name}: {channel}")


    @commands.command(name='list-channels')
    @commands.has_any_role('mod', '@mod')
    async def listChannels(self, ctx):
        for channel in self.db[str(ctx.guild.id)]:
            channel_name = self.bot.get_channel(id=int(channel))
            print(f"{channel_name}")
            await ctx.send(f"{channel_name}")


    @commands.command(name='del-hist')
    @commands.has_any_role('mod', '@mod')
    async def delHistory(self, ctx, *args):
        channels = await self.filter_channels(ctx, args)
        srv_id = str(ctx.guild.id)
        server = self.db[srv_id]

        # if 0 args, delete everything
        if len(args) == 0:
            print(f"deleting saved history of all channels")
            await ctx.send(f"deleting saved history of all channels")
            self.db[srv_id] = {}
            return

        for channel in channels:
            print(f"deleting saved history of {channel}")
            await ctx.send(f"deleting saved history of {channel}")
            del server[channel.id]
        self.db[srv_id] = server


    @commands.command(name='add-hist')
    @commands.has_any_role('mod', '@mod')
    async def getHistory(self, ctx, *args):
        channels = await self.filter_channels(ctx, args)

        # if server has not been saved in the db initialize it
        srv_id   = str(ctx.guild.id)
        if srv_id not in self.db: 
            self.db[srv_id] = {}

        # TODO fix this
        for arg in args:
            if arg not in [i for i in channels]:
                print(f"no channel named {arg}")
                await ctx.send(f"no channel named {arg}")

        for channel in channels:
            print(f"Grabbing messages from {channel} this could take a while...")
            await ctx.send(f"Grabbing messages from {channel} this could take a while...")

            history  = await channel.history(limit=None, oldest_first=True).flatten()
            filtered = await self.filter_messages(history)

            # store channel history in server entry
            srv_dict = self.db[srv_id]
            srv_dict[channel.id] = filtered
            self.db[srv_id] = srv_dict

            print(f"Grabbed {len(filtered)} messages from {channel}")
            await ctx.send(f"Grabbed {len(filtered)} messages from {channel}")



    async def filter_channels(self, ctx, requested_channels):
        """ 
        Given a list of channels, returns the ones that actually exist
        If no arguments are given, return all channels
        """
        channels = ctx.guild.text_channels
        new_channels = []
        if len(requested_channels) == 0: # if no channels specified grab them all
            return channels

        for channel in channels:
            if channel.name in requested_channels:
                new_channels.append(channel)
        return new_channels
        

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
