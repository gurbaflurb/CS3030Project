from textblob import TextBlob
from discord.ext import commands
import discord
import random
import shelve

class TextEmotion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = shelve.open('emotion.db')

    @commands.command(name="gen-emotion")
    async def gen_emotion(self, ctx):
        srv_id = str(ctx.guild.id)
        await self.generate_emotion_db(srv_id)


    async def generate_emotion_db(self, srv_id):
        history  = self.bot.get_cog('History')
        messages = await history.get_history(srv_id)

        emotion_db = {}
        for msg in messages:
            category = await self.get_emotion(msg)
            if category not in emotion_db:
                emotion_db[category] = [msg]
            else:
                emotion_db[category] += [msg]

        self.db[srv_id] = emotion_db
        print("Created emotion db")

    async def get_messages(self, srv_id, emotion=None, subjective=None):
        server = self.db[srv_id]
        history = []

        for category, messages in server.items():
            if ((category[0] == emotion or emotion is None)
                    and (category[1] == subjective or subjective is None)):
                history += messages

        return history

    async def get_rand_message(self, srv_id, emotion=None, subjective=None):
        messages  = await self.get_messages(srv_id, emotion, subjective)
        rand_msgs = [random.choice(messages)]
        return tuple(rand_msgs)
        

    async def get_emotion(self, *args):
        blob = TextBlob(' '.join(args))
        blob.tags
        blob.noun_phrases

        totalSentences = 0
        totalSubjectivity = 0
        totalPolarity = 1
        for sentence in blob.sentences:
            totalSubjectivity += sentence.sentiment.subjectivity
            totalPolarity += sentence.sentiment.polarity
            totalSentences += 1

        subjectivity = totalSubjectivity/totalSentences
        polarity = totalPolarity/totalSentences
        emotion = ''
        if polarity > 1.5:
            emotion = 'Happy'
        elif polarity >= 1 and polarity < 1.5:
            emotion = "Neutral"
        elif polarity < 1:
            emotion = "Sad"
        
        subjective = ''
        if subjectivity > .8:
            subjective = "Opinion"
        elif subjectivity < .8 and subjectivity > .6:
            subjective = "Neither"
        elif subjectivity < .6:
            subjective = "Fact"

        return emotion, subjective
    
