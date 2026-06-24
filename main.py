import discord
from discord.ext import commands
import datetime
import os

intents = discord.Intents.default()
intents.message_content = True # THIS IS CRITICAL
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- DEBUGGING / ERROR HANDLING ---
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("❌ **ACCESS DENIED:** You lack the authorization (Judge Role) to issue this command.")
    elif isinstance(error, commands.CommandNotFound):
        pass # Ignore unknown commands
    else:
        await ctx.send(f"⚠️ **ERROR:** {str(error)}")

@bot.event
async def on_ready():
    print(f"Empire Court Bot Active as {bot.user}")

# --- TEST COMMAND ---
@bot.command()
async def ping(ctx):
    """Simple test to see if the bot is alive."""
    await ctx.send("⚖️ The Empire is listening.")

# --- YOUR EXISTING COMMANDS ---
# (Keep your !trial and !verdict commands here as they were before)

# TO TEST, REPLACE THE TOKEN BELOW WITH YOUR ACTUAL STRING IF ENVIRONMENT VARIABLES FAIL
TOKEN = os.getenv('DISCORD_TOKEN') 
bot.run(TOKEN)
