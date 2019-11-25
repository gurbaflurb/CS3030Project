'''
This file does stuff with history. If anything has to do with the history, this is where it would be defined
'''

import discord
import random

'''
getHistory function takes a message in the form of '!history numericalValueHere' and returns a history of messages to the user. If the user inputs
an invalid character for the numerical value, the function will return None
'''
async def getHistory(message):
	if len(message.content) > 8:
		num = message.content[8:]
	else:
		num = 100
	try:
		num = int(num)
		history = await message.channel.history(limit=150).flatten()
		returnHistory = []
		for chatMsg in history:
			if('!history' in chatMsg.content or chatMsg.content == ''):
				num = num+1
				continue
			else:
				returnHistory.append(chatMsg.content)
		return returnHistory
	except ValueError:
		return None

async def spongeBobText(message):
	if(message.content == '!spongebob'):
		history = await message.channel.history(limit=100).flatten()
		for word in history:
			if(word.content.startswith('!spongebob')):
				continue
			else:
				tempText = word.content
				break
		returnChar = ''
		for character in tempText:
			randValue = random.randint(0,1)
			if(randValue == 0):
				returnChar = returnChar + character.upper()
			else:
				returnChar = returnChar+character
		return returnChar


				