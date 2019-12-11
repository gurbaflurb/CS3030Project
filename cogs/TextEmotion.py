from textblob import TextBlob
from discord.ext import commands
import discord
import random

class TextEmotion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


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
    
    async def get_text(self, srv_id: str, emotion, objectivness):
        hist_cog = self.bot.get_cog('History')
        rand_msg = await hist_cog.get_random_messages(srv_id, 1)

        catagory  = await self.get_emotion(rand_msg[0])
        rand_emotion      = catagory[0]
        rand_objectivness = catagory[1]

        if ((rand_objectivness == objectivness or objectivness is None)
            and (rand_emotion == emotion or emotion is None)):
            print(rand_emotion, rand_objectivness)
            return rand_msg
        else:
            return await self.get_text(srv_id, emotion, objectivness)

        
        
