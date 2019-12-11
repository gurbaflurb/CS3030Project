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


    @commands.command(name='list-markov')
    @commands.has_any_role('mod', '@mod')
    async def list_markov(self, ctx):
        for key in self.db.keys():
            server_name = self.bot.get_guild(id=int(key)).name
            print(f"{server_name}: {key}")

    @list_markov.error
    async def list_markov_error(self, ctx, error):
        await ctx.send("Looks like an error occured:\n f{error}")
        

    @commands.command(name='gen-markov')
    @commands.has_any_role('mod', '@mod')
    async def call_generate_markov(self, ctx):
        srv_id = str(ctx.guild.id)
        await self.generate_markov(srv_id)
        await ctx.send("Generated markov chain object for this server")

    @call_generate_markov.error
    async def call_generate_markov_error(self, ctx, error):
        await ctx.send("Looks like an error occured:\n f{error}")


    async def generate_markov(self, *args):
        hist_cog = self.bot.get_cog('History')
        for srv_id in args:
            await hist_cog.get_history(srv_id, as_text=True)

            with open("history_temp.txt", "r") as f:
                text = f.read()
            self.db[srv_id] = markovify.NewlineText(text)


    async def get_chain(self, srv_id: str, num: int):
        rand_msgs = []
        server = self.db[srv_id]
        for i in range(num):
            rand_msgs += [server.make_short_sentence(100, tries=20)]

        return rand_msgs
