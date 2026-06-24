import discord
from discord.ext import commands
import datetime
import os

# --- SETUP ---
intents = discord.Intents.default()
intents.message_content = True  # MANDATORY FOR COMMANDS
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- CONFIGURATION (UPDATE THESE) ---
# Right-click your Role -> Copy Role ID
JUDGE_ROLE_ID = 123456789012345678  
# Right-click your Channels -> Copy Channel ID
VAULT_CHANNEL_ID = 123456789012345678 
RECORDS_CHANNEL_ID = 123456789012345678 

# --- AESTHETICS ---
BLACK = 0x000000
GOLD = 0xFFD700
WHITE = 0xFFFFFF

@bot.event
async def on_ready():
    print(f"Empire Court Bot is active: {bot.user}")

# --- ERROR HANDLING (STOPS SILENT FAILURES) ---
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("❌ **AUTHORIZATION DENIED:** You lack the required Judge credentials.")
    elif isinstance(error, commands.CommandNotFound):
        pass # Ignore invalid commands
    else:
        await ctx.send(f"⚠️ **SYSTEM ERROR:** {str(error)}")

# --- COMMANDS ---
@bot.command()
async def ping(ctx):
    """Test command to see if the bot is alive."""
    await ctx.send("⚖️ The Empire is listening.")

@bot.command()
@commands.has_role(JUDGE_ROLE_ID)
async def trial(ctx, defendant: discord.Member, *, charge: str):
    """Starts a new court case."""
    case_num = f"CASE-{datetime.datetime.now().strftime('%H%M')}"
    
    embed = discord.Embed(title="⚖️ COURT OF THE EMPIRE: SESSION OPENED", color=WHITE)
    embed.add_field(name="CASE NUMBER", value=case_num, inline=True)
    embed.add_field(name="DEFENDANT", value=defendant.mention, inline=True)
    embed.add_field(name="CHARGE", value=charge, inline=False)
    embed.set_footer(text="Proceedings are classified until verdict.")
    
    thread = await ctx.channel.create_thread(name=f"{case_num} | {defendant.name}", type=discord.ChannelType.private_thread)
    await thread.send(embed=embed)
    await ctx.send(f"**{case_num}** has been registered. The court is in session: {thread.mention}")

@bot.command()
@commands.has_role(JUDGE_ROLE_ID)
async def verdict(ctx, charges: str, status: str, *, disposition: str):
    """Closes the case and records the judgment."""
    vault = bot.get_channel(VAULT_CHANNEL_ID)
    records = bot.get_channel(RECORDS_CHANNEL_ID)
    
    if not vault or not records:
        return await ctx.send("❌ **CONFIG ERROR:** Records or Vault channel not found.")
        
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Secure/Classified Record (Vault)
    embed_vault = discord.Embed(title="🔒 IMPERIAL VAULT RECORD", color=BLACK)
    embed_vault.add_field(name="CASE", value=ctx.channel.name, inline=True)
    embed_vault.add_field(name="DATE", value=date, inline=True)
    embed_vault.add_field(name="CHARGES", value=charges, inline=False)
    embed_vault.add_field(name="STATUS", value=status, inline=True)
    embed_vault.add_field(name="DISPOSITION", value=disposition, inline=False)
    await vault.send(embed=embed_vault)

    # Public Record (Records)
    embed_public = discord.Embed(title="📜 EMPIRE ARCHIVE: CASE CLOSED", color=GOLD)
    embed_public.add_field(name="CASE", value=ctx.channel.name, inline=True)
    embed_public.add_field(name="DATE", value=date, inline=True)
    embed_public.add_field(name="VERDICT", value=status, inline=False)
    await records.send(embed=embed_public)

    await ctx.send("Verdict processed. Records sealed.")
    await ctx.channel.edit(archived=True, locked=True)

# Replace 'YOUR_BOT_TOKEN_HERE' if not using environment variables
bot.run(os.getenv('DISCORD_TOKEN'))

