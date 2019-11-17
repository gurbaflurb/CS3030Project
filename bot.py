#!/usr/bin/python3

import discord

from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if(message.author == client.user):
		return

	if message.content.startswith('$hello'):
		await message.channel.send('Hello!')

print('Please enter the Authentication Token')

client.run(token)
