# CS3030Project
Our project for this semester was to build a Discord bot using python. Our bot will be able to generate memes based on user input, there will also be parameters to change or set the meme image background. We are also planning on adding the ability for the bot to make Markov Chains out of user messages sent to the server. We are also planning on adding an optional word filter to remove messages that include certain words.

## Setup your own Bot
- Go through the process of adding a bot in the discord developer portal: https://discordapp.com/developers/applications/
- Then add the bot using the OAuth2 menu to get the bot url
- Copy the token for the bot to login with under the Bot menu
- In the directory where all these files are located, make a file called `.env`, and put the following inside of it:
```
DISCORD_TOKEN="Put your OAuth2 Code here"
DISCORD_GUILD="NameOfBot"
MEME_TEMPLATE_DIR="template_images"
IMAGE_DIR="images"
DEFAULT_FONT="fonts/comicsansms3.ttf"
TEMP_IMAGE="temp.jpg"
GLOBAL_IMAGE_DIR="images/global"
```

Also make sure to make the \$IMAGE_DIR folder and the \$GLOBAL_IMAGE_DIR folder and add at least one image in the \$GLOBAL_IMAGE_DIR folder.

### Windows Server
- On the server you need to run the command `py -3 -m pip install -r requirements.txt`. This will install the dependencies and packages you will need to run this bot.
- Then you can run the command `py -3 bot.py` on the commandline in Windows to run the bot. The bot should begin running and will automatically connect to your server.

### Linux Server
- On the server you need to run the command `python3 -m pip install -r requirements.txt`. This will install the dependencies and packages you will need to run this bot.
- Then you can run the command `python3 bot.py` on the Linux terminal to run the bot. The bot should begin running and will automatically connect to your server.

## Todo
* handle permissions errors when grabbing from channels 
* fix channel not deleting
