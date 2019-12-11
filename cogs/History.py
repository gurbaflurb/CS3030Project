from discord.ext import commands
import discord
import os
import random
import shelve
from dotenv import load_dotenv

load_dotenv()

class History(commands.Cog):
    """
    if a variable is named channel or channels they should be a channel object.
    If a variable is a channel name or id the variable should have the word id
    or name in it
    """

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

    @listHistory.error
    async def listHistory_error(self, ctx, error):
        await ctx.channel.send(f"Something went wrong, here's an error message:\nf{error}")
    

    @commands.command(name='list-channels')
    @commands.has_any_role('mod', '@mod')
    async def listChannels(self, ctx):
        for channel_id in self.db[str(ctx.guild.id)]:
            channel_name = self.bot.get_channel(id=int(channel_id))
            print(f"{channel_name}")
            await ctx.send(f"{channel_name}")


    @commands.command(name='add-channel')
    @commands.has_any_role('mod', '@mod')
    async def save_channels(self, ctx, *args):
        if len(args) == 0:
            print("No channels specified")
            await ctx.send("No channels specified")

        channel_ids = await self.get_channel_ids(ctx, args)
        await self.save_history(ctx, channel_ids)


    @commands.command(name='add-all')
    @commands.has_any_role('mod', '@mod')
    async def save_all_channels(self, ctx):
        channel_ids = [i.id for i in ctx.guild.text_channels]
        await self.save_history(ctx, channel_ids)


    @commands.command(name='del-channel')
    @commands.has_any_role('mod', '@mod')
    async def delete_channels(self, ctx, *args):
        if len(args) == 0:
            print("No channels specified")
            await ctx.send("No channels specified")

        channel_ids = await self.get_channel_ids(ctx, args)
        await self.delete_history(ctx, channel_ids)


    @commands.command(name='del-all')
    @commands.has_any_role('mod', '@mod')
    async def delete_all_channels(self, ctx):
        await self.delete_history(ctx, [], del_all=True)


    @commands.command(name='clean-channels')
    @commands.has_any_role('mod', '@mod')
    async def clean_channels(self, ctx):
        srv_id = ctx.guild.id
        db_channels = self.db[str(srv_id)]

        server_channel_ids = [i.id for i in ctx.guild.text_channels]
        removed_channel_ids = []

        for channel_id in db_channels.keys():
            if channel_id not in server_channel_ids:
                removed_channel_ids.append(channel_id) 

        await self.delete_history(ctx, removed_channel_ids)


    async def save_history(self, ctx, channel_ids: list):
        # if server has not been saved in the db initialize it
        srv_id   = str(ctx.guild.id)
        if srv_id not in self.db: 
            self.db[srv_id] = {}

        for channel_id in channel_ids:
            channel = self.bot.get_channel(channel_id)
            print(f"Grabbing messages from {channel} this could take a while...")
            await ctx.send(f"Grabbing messages from {channel} this could take a while...")

            history  = await channel.history(limit=None, oldest_first=True).flatten()
            filtered = await self.filter_messages(history)

            # store channel history in server entry
            srv_dict = self.db[srv_id]
            srv_dict[channel_id] = filtered
            self.db[srv_id] = srv_dict

            print(f"Grabbed {len(filtered)} messages from {channel}")
            await ctx.send(f"Grabbed {len(filtered)} messages from {channel}")


    async def delete_history(self, ctx, channel_ids, del_all=False):
        srv_id = str(ctx.guild.id)
        server = self.db[srv_id]

        if del_all:
            print(f"deleting saved history of all channels")
            await ctx.send(f"deleting saved history of all channels")
            self.db[srv_id] = {}
            return

        for channel_id in channel_ids:
            channel = self.bot.get_channel(id=int(channel_id))
            if channel != None:
                print(f"deleting saved history of {channel}")
                await ctx.send(f"deleting saved history of {channel}")
            else:
                print(f"deleting saved history of a removed channel")
                await ctx.send(f"deleting saved history of a removed channel")

            del server[channel_id]
        self.db[srv_id] = server


    async def get_channel_ids(self, ctx, requested_channels):
        """ 
        Given a list of channels names, return the channel ids that actually 
        exist
        """
        channels = ctx.guild.text_channels
        channel_names     = [x.name for x in channels]
        invalid_channels  = [x for x in requested_channels if x not in channel_names]
        valid_channel_ids = []

        for channel in channels:
            if channel.name in requested_channels:
                valid_channel_ids.append(channel.id)

        for channel_name in invalid_channels:
                print(f"channel {channel_name} does not exist")
                await ctx.send(f"channel {channel_name} does not exist")
        return valid_channel_ids
        

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


    async def get_history(self, srv_id: str, as_text=False):
        server = self.db[srv_id]
        history = []
        for channel_history in server.values():
            history += channel_history

        if not as_text:
            return history
        else:
            f = open("history_temp.txt", "w")
            f.write('\n'.join(history))
            f.close()

    @commands.command(name='hist-text')
    @commands.has_any_role('mod', '@mod')
    async def text_hist(self, ctx):
        srv_id = str(ctx.guild.id)
        await self.get_history(srv_id, as_text=True)


    async def get_random_messages(self, ctx, num: int):
        srv_id = str(ctx.guild.id)
        messages  = await self.get_history(srv_id)
        rand_msgs = [random.choice(messages) for i in range(num)]
        return tuple(rand_msgs)
