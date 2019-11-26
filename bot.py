#!./bin/python3

import discord
import history
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
	print('We have logged in as {0.user}'.format(bot))

@bot.command(name='echo')
async def echo(ctx, *args):
	await ctx.send(' '.join(args))

@echo.error
async def echo_error(ctx, error):
	await ctx.send("You didn't give me anything to echo ಥ_ಥ")

@bot.command(name='history')
async def getHistory(ctx, arg: int):
	history = await ctx.history(limit=arg).flatten()
	print(type(history.content))
	returnHistory = []
	for chatMsg in history:
		if('!history' in chatMsg.content or chatMsg.content == ''):
			num = num+1
			continue
		else:
			returnHistory.append(chatMsg.content)
	await ctx.send(returnHistory)

@getHistory.error
async def history_error(ctx, error):
	if isinstance(error, commands.ArgumentParsingError):
		await ctx.send("You didn't give me valid arguments ಥ_ಥ")
		

'''
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
'''
print('Please enter the Authentication Token')
token = input()
bot.run(token)