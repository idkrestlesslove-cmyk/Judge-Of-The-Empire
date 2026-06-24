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
# PASTE YOUR CORRECT ROLE ID HERE (from !debugroles)
JUDGE_ROLE_ID = 000000000000000000 
# PASTE YOUR CHANNEL IDs HERE
VAULT_CHANNEL_ID = 000000000000000000 
RECORDS_CHANNEL_ID = 000000000000000000 

# --- AESTHETICS ---
BLACK = 0x000000
GOLD = 0xFFD700
WHITE = 0xFFFFFF

@bot.event
async def on_ready():
    print(f"Empire Court System Active: {bot.user}")

# --- DIAGNOSTICS & ERROR HANDLING ---
@bot.command()
async def debugroles(ctx):
    output = "Here are your role IDs:\n"
    for role in ctx.author.roles:
        output += f"**{role.name}**: `{role.id}`\n"
    await ctx.send(output)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("❌ **ACCESS DENIED:** You lack the required Judge credentials.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("❌ **BOT ERROR:** I do not have 'Manage Threads' permission.")
    else:
        await ctx.send(f"⚠️ **ERROR:** {str(error)}")

# --- COURT COMMANDS ---
@bot.command()
async def ping(ctx):
    await ctx.send("⚖️ The Empire is listening.")

@bot.command()
@commands.has_role(JUDGE_ROLE_ID)
async def trial(ctx, defendant: discord.Member, *, charge: str):
    case_num = f"CASE-{datetime.datetime.now().strftime('%H%M')}"
    
    # Create Private Thread
    thread = await ctx.channel.create_thread(name=f"{case_num} | {defendant.name}", type=discord.ChannelType.private_thread)

    embed = discord.Embed(title="⚖️ COURT OF THE EMPIRE: SESSION OPENED", color=WHITE)
    embed.add_field(name="CASE NUMBER", value=case_num, inline=True)
    embed.add_field(name="DEFENDANT", value=defendant.mention, inline=True)
    embed.add_field(name="CHARGE", value=charge, inline=False)
    embed.set_footer(text="Proceedings are classified until verdict.")
    
    await thread.send(embed=embed)
    await ctx.send(f"**{case_num}** registered. Court is in session: {thread.mention}")

@bot.command()
@commands.has_role(JUDGE_ROLE_ID)
async def verdict(ctx, charges: str, status: str, *, disposition: str):
    vault = bot.get_channel(VAULT_CHANNEL_ID)
    records = bot.get_channel(RECORDS_CHANNEL_ID)
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Vault Record (Black)
    if vault:
        embed_vault = discord.Embed(title="🔒 IMPERIAL VAULT RECORD", color=BLACK)
        embed_vault.add_field(name="CASE", value=ctx.channel.name, inline=True)
        embed_vault.add_field(name="DATE", value=date, inline=True)
        embed_vault.add_field(name="CHARGES", value=charges, inline=False)
        embed_vault.add_field(name="STATUS", value=status, inline=True)
        embed_vault.add_field(name="DISPOSITION", value=disposition, inline=False)
        await vault.send(embed=embed_vault)

    # Public Archive (Gold)
    if records:
        embed_public = discord.Embed(title="📜 EMPIRE ARCHIVE: CASE CLOSED", color=GOLD)
        embed_public.add_field(name="CASE", value=ctx.channel.name, inline=True)
        embed_public.add_field(name="DATE", value=date, inline=True)
        embed_public.add_field(name="VERDICT", value=status, inline=False)
        await records.send(embed=embed_public)

    await ctx.send("Verdict processed. Records sealed.")
    await ctx.channel.edit(archived=True, locked=True)

bot.run(os.getenv('DISCORD_TOKEN'))
