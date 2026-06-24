import discord
from discord.ext import commands
import datetime
import os

# --- SETUP ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True # Essential for seeing roles
bot = commands.Bot(command_prefix="!", intents=intents)

# --- CONFIGURATION (UPDATE THESE) ---
JUDGE_ROLE_ID = 123456789012345678  # UPDATE ME
VAULT_CHANNEL_ID = 123456789012345678 # UPDATE ME
RECORDS_CHANNEL_ID = 123456789012345678 # UPDATE ME

# --- DIAGNOSTIC COMMAND ---
@bot.command()
async def myroles(ctx):
    """Debug tool: Tells you what roles the bot sees on your account."""
    roles = [role.name for role in ctx.author.roles]
    await ctx.send(f"**The bot sees these roles on your account:**\n{', '.join(roles)}")

# --- ERROR HANDLING ---
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("❌ **ACCESS DENIED:** You lack the Judge Role ID required to execute this command.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("❌ **BOT ERROR:** I do not have permission to create threads/manage channels in this server.")
    else:
        print(f"Error: {error}") # Prints to your terminal window
        await ctx.send(f"⚠️ **ERROR:** {str(error)}")

# --- COMMANDS ---
@bot.command()
async def ping(ctx):
    await ctx.send("⚖️ The Empire is listening.")

@bot.command()
@commands.has_role(JUDGE_ROLE_ID)
async def trial(ctx, defendant: discord.Member, *, charge: str):
    """Starts a new court case."""
    case_num = f"CASE-{datetime.datetime.now().strftime('%H%M')}"
    
    # Check if we can create threads
    try:
        thread = await ctx.channel.create_thread(name=f"{case_num} | {defendant.name}", type=discord.ChannelType.private_thread)
    except discord.Forbidden:
        return await ctx.send("❌ **CRITICAL ERROR:** I do not have 'Manage Threads' permission in this channel.")

    embed = discord.Embed(title="⚖️ COURT OF THE EMPIRE: SESSION OPENED", color=0xFFFFFF)
    embed.add_field(name="CASE NUMBER", value=case_num, inline=True)
    embed.add_field(name="DEFENDANT", value=defendant.mention, inline=True)
    embed.add_field(name="CHARGE", value=charge, inline=False)
    
    await thread.send(embed=embed)
    await ctx.send(f"**{case_num}** registered. Court is in session: {thread.mention}")

@bot.command()
@commands.has_role(JUDGE_ROLE_ID)
async def verdict(ctx, charges: str, status: str, *, disposition: str):
    vault = bot.get_channel(VAULT_CHANNEL_ID)
    records = bot.get_channel(RECORDS_CHANNEL_ID)
    
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Vault
    if vault:
        embed_vault = discord.Embed(title="🔒 IMPERIAL VAULT RECORD", color=0x000000)
        embed_vault.add_field(name="CASE", value=ctx.channel.name, inline=True)
        embed_vault.add_field(name="CHARGES", value=charges, inline=False)
        embed_vault.add_field(name="DISPOSITION", value=disposition, inline=False)
        await vault.send(embed=embed_vault)

    # Records
    if records:
        embed_public = discord.Embed(title="📜 EMPIRE ARCHIVE: CASE CLOSED", color=0xFFD700)
        embed_public.add_field(name="CASE", value=ctx.channel.name, inline=True)
        embed_public.add_field(name="VERDICT", value=status, inline=False)
        await records.send(embed_public)

    await ctx.send("Verdict processed. Records sealed.")
    await ctx.channel.edit(archived=True, locked=True)

bot.run(os.getenv('DISCORD_TOKEN'))


