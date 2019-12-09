from discord.ext import commands
import discord
import shelve
import markovify
from dotenv import load_dotenv

load_dotenv()

class Markov(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db = shelve.open('markov.db')

    @commands.command(name='gen-markov')
    @commands.has_any_role('mod', '@mod')
    async def call_generate_markov(self, ctx, *args):
        await self.generate_markov(ctx)
        await ctx.send("Generated markov chain object for this server")

    async def generate_markov(self, ctx, *args):
        hist_cog = self.bot.get_cog('History')
        await hist_cog.get_history(ctx, as_text=True)

        with open("history_temp.txt", "r") as f:
            text = f.read()

        srv_id = str(ctx.guild.id)
        self.db[srv_id] = markovify.Text(text)


    async def get_chain(self, ctx, num: int):
        rand_msgs = []
        srv_id = str(ctx.guild.id)
        server = self.db[srv_id]
        for i in range(num):
            rand_msgs += [server.make_short_sentence(100)]

        return rand_msgs
