from typing import Final

import discord
import choice_buttons

import os
import blackjackgame
import audiofunctionality

from dotenv import load_dotenv;

# This script initializes the discord bot
# Calls seperate scripts for different functionality based on user input

# Load environment variables from .env file
load_dotenv();
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN');

# Create intents to enable message content access
intents = discord.Intents.default();
intents.message_content = True;

client = discord.Client(intents=intents);

# Store instances of blackjack games
active_games = {};

# Message ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user}');

# On Message
@client.event
async def on_message(message):
    # If no error:
    try:
        print(f"Received message: {message.content}")  # Log received messages

        # Ignore messages sent by bot
        if message.author == client.user:
            return;

        # If message contains !blackjack
        # Start blackjack functionality
        if message.content.startswith('!blackjack'):
            # Store player
            player = message.author;

            # Store channel
            location = message.channel;

            # Check if user in active game or not
            user = message.author.id;
            if user in active_games:
                await message.channel.send("You're already in a game!");
                return;
            active_games[user] = True;
            try:
                await blackjackgame.main(message);
            finally:
                del active_games[user];
    
        # Open music commands
        #if message.content.startswith('!music'):
        #    if message.author.voice is None:
        #        await message.channel.send("User not in voice channel");
        #    else:
                # Run audio player script
        #        await audiofunctionality.main(message);

    # If error:
    except Exception as e:
        print(f"Error processing message: {e}");

# Signing Bot in
if TOKEN:
    client.run(TOKEN)  # This line signs the bot in!
else:
    print("No token found in the environment variables.");