import discord
from discord.ext import commands
import datetime
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True 
bot = commands.Bot(command_prefix="!", intents=intents)

# --- CONFIGURATION ---
JUDGE_ROLE_ID = 1519179704500748388 
BUNKER_CHANNEL_ID = 1519313838481080390
RECORDS_CHANNEL_ID = 1519338155441131601

@bot.command()
@commands.has_role(JUDGE_ROLE_ID)
async def verdict(ctx, charges: str, status: str, *, disposition: str):
    bunker = bot.get_channel(BUNKER_CHANNEL_ID)
    records = bot.get_channel(RECORDS_CHANNEL_ID)
    
    # 1. Bunker Transmission
    try:
        await bunker.send(embed=discord.Embed(title="🔒 BUNKER-RECORDS", color=0x000000, 
                          description=f"Case: {ctx.channel.name}\nStatus: {status}\nCharges: {charges}\nDisposition: {disposition}"))
    except Exception as e:
        await ctx.send(f"❌ BUNKER FAILED: {e}")

    # 2. Archive Transmission
    try:
        await records.send(embed=discord.Embed(title="📜 EMPIRE ARCHIVE: CASE CLOSED", color=0xFFD700,
                           description=f"Case: {ctx.channel.name}\nVerdict: {status}"))
    except Exception as e:
        await ctx.send(f"❌ RECORDS FAILED: {e}")

    # 3. Thread Closure
    try:
        await ctx.channel.edit(archived=True, locked=True)
        await ctx.send("✅ Verdict processed. Records sealed and thread closed.")
    except Exception as e:
        await ctx.send(f"❌ THREAD CLOSE FAILED: {e}")

bot.run(os.getenv('DISCORD_TOKEN'))
