import discord
from discord.ext import commands
import datetime
import os

# --- SETUP ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True 
bot = commands.Bot(command_prefix="!", intents=intents)

# --- CONFIGURATION ---
JUDGE_ROLE_ID = 1519179704500748388 
BUNKER_CHANNEL_ID = 1519313838481080390
RECORDS_CHANNEL_ID = 1519338155441131601

# --- AESTHETICS ---
BLACK = 0x000000
GOLD = 0xFFD700
WHITE = 0xFFFFFF

@bot.event
async def on_ready():
    print(f"Empire Court System Online. Ready for duty.")

# --- DIAGNOSTIC TOOL ---
@bot.command()
async def checkchannels(ctx):
    """Checks if the bot can find and access the configured channels."""
    bunker = bot.get_channel(BUNKER_CHANNEL_ID)
    records = bot.get_channel(RECORDS_CHANNEL_ID)
    
    msg = "**Empire Channel Status Report:**\n"
    msg += f"Bunker-Records: {'✅ Found (' + bunker.name + ')' if bunker else '❌ NOT FOUND'}\n"
    msg += f"Court Records: {'✅ Found (' + records.name + ')' if records else '❌ NOT FOUND'}\n"
    
    await ctx.send(msg)

# --- ERROR HANDLING ---
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("❌ **ACCESS DENIED:** You lack the required Judge credentials.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ **SYNTAX ERROR:** Use quotes for multi-word arguments.")
    else:
        print(f"Error: {error}")
        await ctx.send(f"⚠️ **ERROR:** {str(error)}")

# --- COURT COMMANDS ---
@bot.command()
async def ping(ctx):
    await ctx.send("⚖️ The Empire is listening.")

@bot.command()
@commands.has_role(JUDGE_ROLE_ID)
async def trial(ctx, defendant: discord.Member, *, charge: str):
    case_num = f"CASE-{datetime.datetime.now().strftime('%H%M')}"
    
    thread = await ctx.channel.create_thread(name=f"{case_num} | {defendant.name}", type=discord.ChannelType.private_thread)

    embed = discord.Embed(title="⚖️ COURT OF THE EMPIRE: SESSION OPENED", color=WHITE)
    embed.add_field(name="CASE NUMBER", value=case_num, inline=True)
    embed.add_field(name="DEFENDANT", value=defendant.mention, inline=True)
    embed.add_field(name="CHARGE", value=charge, inline=False)
    
    await thread.send(embed=embed)
    await ctx.send(f"**{case_num}** registered. Court is in session: {thread.mention}")

@bot.command()
@commands.has_role(JUDGE_ROLE_ID)
async def verdict(ctx, charges: str, status: str, *, disposition: str):
    bunker = bot.get_channel(BUNKER_CHANNEL_ID)
    records = bot.get_channel(RECORDS_CHANNEL_ID)
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Send to Bunker
    if bunker:
        try:
            embed_bunker = discord.Embed(title="🔒 BUNKER-RECORDS", color=BLACK)
            embed_bunker.add_field(name="CASE", value=ctx.channel.name, inline=True)
            embed_bunker.add_field(name="STATUS", value=status, inline=True)
            embed_bunker.add_field(name="CHARGES", value=charges, inline=False)
            embed_bunker.add_field(name="DISPOSITION", value=disposition, inline=False)
            await bunker.send(embed=embed_bunker)
        except Exception as e:
            await ctx.send(f"⚠️ Bunker send failed: {e}")

    # Send to Records
    if records:
        try:
            embed_public = discord.Embed(title="📜 EMPIRE ARCHIVE: CASE CLOSED", color=GOLD)
            embed_public.add_field(name="CASE", value=ctx.channel.name, inline=True)
            embed_public.add_field(name="VERDICT", value=status, inline=False)
            await records.send(embed=embed_public)
        except Exception as e:
            await ctx.send(f"⚠️ Records send failed: {e}")
    else:
        await ctx.send("❌ Critical Error: Records channel ID not found.")

    await ctx.send("Verdict processed. Records sealed.")
    await ctx.channel.edit(archived=True, locked=True)

bot.run(os.getenv('DISCORD_TOKEN'))
