from discord.ext import commands
import discord
from dotenv import load_dotenv

class admin(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='reload', hidden=True)
    async def _reload(self, ctx, *, arg):
        try:
            self.bot.reload_extension(arg)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send('Reloaded {}'.format(arg))

    @commands.command(name='ban', hidden=True)
    async def _ban(self, ctx, *, arg):
        pass

    async def word_filter(message):
        banned_words = ['fuck', 'shit', 'asshole','kys',]# List of banned words
        for word in banned_words:
            if word in message.content:
                await message.delete()