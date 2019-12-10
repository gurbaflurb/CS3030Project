from discord.ext import commands
import discord
import os
import shelve
from textblob import TextBlob
from dotenv import load_dotenv

load_dotenv()

class Emotion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="emotion")
    async def getEmotion(self, ctx, *args):
        blob = TextBlob(' '.join(args))
        blob.tags
        blob.noun_phrases

        for sentence in blob.sentences:
            print(sentence.sentiment.polarity)

