#!/usr/bin/python3
import discord, os
from discord.ext import commands
from dotenv import load_dotenv

# Local Files
from cogs.Memes import Memes
from cogs.FunAndGames import FunAndGames
from cogs.History import History
from cogs.admin import admin

# load environment variables (relavent ones are stored in .env)
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# create bot object (subclass of client object)
bot = commands.Bot(command_prefix='!')
bot.add_cog(Memes(bot))
bot.add_cog(FunAndGames(bot))
bot.add_cog(History(bot))
bot.add_cog(admin(bot))
bot.add_listener(admin.word_filter)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

bot.run(token)

