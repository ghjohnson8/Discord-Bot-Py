import discord
from discord.ext import commands
from discord.ui import View, Button

# This script stores button presets for prompting the user:

# Hit Buttons - Prompt the user to either hit, stand, or quit
# Start Buttons - Prompt the user to either start a game or exit

# Game Buttons (Hit, Stand, Quit)
class Hit_Buttons(View):
    def __init__(self):
        super().__init__();
        self.result = None;  # Store the choice

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return True;  # Ensures any user can interact

    # Hit
    @discord.ui.button(label="Hit", style=discord.ButtonStyle.green)
    async def hit(self, interaction: discord.Interaction, button: Button):
        self.result = "hit";
        await interaction.response.defer();  # Acknowledge interaction without changing message
        self.stop();  # Stop waiting for more interactions

    # Stand
    @discord.ui.button(label="Stand", style=discord.ButtonStyle.blurple)
    async def stand(self, interaction: discord.Interaction, button: Button):
        self.result = "stand";
        await interaction.response.defer();
        self.stop();

    # Quit
    @discord.ui.button(label="Quit", style=discord.ButtonStyle.red)
    async def quit(self, interaction: discord.Interaction, button: Button):
        self.result = "quit";
        await interaction.response.defer();
        self.stop();

# Start Buttons (Start, Exit)
class Start_Buttons(View):
    def __init__(self):
        super().__init__();
        self.result = None;  # Store the choice

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return True;  # Ensures any user can interact

    @discord.ui.button(label="Start Game", style=discord.ButtonStyle.green)
    async def hit(self, interaction: discord.Interaction, button: Button):
        self.result = "start";
        await interaction.response.defer();  # Acknowledge interaction without changing message
        self.stop();  # Stop waiting for more interactions

    @discord.ui.button(label="Exit", style=discord.ButtonStyle.red)
    async def stand(self, interaction: discord.Interaction, button: Button):
        self.result = "exit";
        await interaction.response.defer();
        self.stop();

# Play Again Buttons (Again, Quit)
class Play_Again_Buttons(View):
    def __init__(self):
        super().__init__();
        self.result = None;  # Store the choice

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return True;  # Ensures any user can interact

    @discord.ui.button(label="Again", style=discord.ButtonStyle.primary) # primary is blue
    async def hit(self, interaction: discord.Interaction, button: Button):
        self.result = "start";
        await interaction.response.defer();  # Acknowledge interaction without changing message
        self.stop();  # Stop waiting for more interactions

    @discord.ui.button(label="Quit", style=discord.ButtonStyle.red)
    async def stand(self, interaction: discord.Interaction, button: Button):
        self.result = "exit";
        await interaction.response.defer();
        self.stop();