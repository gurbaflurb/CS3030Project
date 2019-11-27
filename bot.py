#!/usr/bin/python3
import discord, os
from discord.ext import commands
from dotenv import load_dotenv

# Local Files
from cogs.Memes import Memes
from cogs.FunAndGames import FunAndGames

# load environment variables (relavent ones are stored in .env)
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# create bot object (subclass of client object)
bot = commands.Bot(command_prefix='!')
bot.add_cog(Memes(bot))
bot.add_cog(FunAndGames(bot))

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='echo')
async def echo(ctx, *args):
	await ctx.send(' '.join(args))

@echo.error
async def echo_error(ctx, error):
	await ctx.send("You didn't give me anything to echo ಥ_ಥ")

bot.run(token)

