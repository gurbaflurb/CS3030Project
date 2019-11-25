#!./bin/python3

import discord
import history

client = discord.Client()

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
	if(message.author == client.user):
		return

	if message.content.startswith('!hello'):
		await message.channel.send('Hello!')
	elif message.content.startswith('!echo'):
		await message.channel.send(message.content[5:])
	elif(message.content.startswith('!history')):
		pastChat = await history.getHistory(message)
		if(pastChat == None):
			await message.channel.send("Invalid number ¯\\_(ツ)_/¯")
		else:
			for msg in pastChat:
				await message.channel.send(msg)
	elif(message.content.startswith('!spongebob')):
		spongebobText = await history.spongeBobText(message)
		if spongebobText == None:
			await message.channel.send("Couldn't find text ¯\\_(ツ)_/¯")
		else:
			await message.channel.send(spongebobText)
		
		

print('Please enter the Authentication Token')
token = input()
client.run(token)