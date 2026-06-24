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

@bot.event
async def on_ready():
    print(f"Empire Court System Online.")

# --- DIAGNOSTIC TOOL ---
@bot.command()
async def debug(ctx):
    """Verifies if the bot has permission to write in target channels."""
    bunker = bot.get_channel(BUNKER_CHANNEL_ID)
    records = bot.get_channel(RECORDS_CHANNEL_ID)
    me = ctx.guild.me
    
    report = "**Empire System Permissions Report:**\n"
    
    # Check Bunker
    if bunker:
        perms = bunker.permissions_for(me)
        status = "✅ OK" if perms.send_messages and perms.embed_links else "❌ MISSING PERMISSIONS"
        report += f"Bunker-Records ({bunker.name}): {status}\n"
    else:
        report += "Bunker-Records: ❌ CHANNEL NOT FOUND\n"
        
    # Check Records
    if records:
        perms = records.permissions_for(me)
        status = "✅ OK" if perms.send_messages and perms.embed_links else "❌ MISSING PERMISSIONS"
        report += f"Court Records ({records.name}): {status}\n"
    else:
        report += "Court Records: ❌ CHANNEL NOT FOUND\n"
        
    await ctx.send(report)

# --- ERROR HANDLING ---
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("❌ **ACCESS DENIED:** You lack the required Judge credentials.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ **SYNTAX ERROR:** Usage: `!verdict \"Charge\" \"Status\" \"Disposition\"`")
    else:
        await ctx.send(f"⚠️ **RUNTIME ERROR:** {str(error)}")

# --- COURT COMMANDS ---
@bot.command()
@commands.has_role(JUDGE_ROLE_ID)
async def trial(ctx, defendant: discord.Member, *, charge: str):
    case_num = f"CASE-{datetime.datetime.now().strftime('%H%M')}"
    thread = await ctx.channel.create_thread(name=f"{case_num} | {defendant.name}", type=discord.ChannelType.private_thread)
    
    embed = discord.Embed(title="⚖️ COURT OF THE EMPIRE: SESSION OPENED", color=0xFFFFFF)
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

    # 1. Bunker Transmission
    if bunker:
        try:
            embed_bunker = discord.Embed(title="🔒 BUNKER-RECORDS", color=0x000000)
            embed_bunker.add_field(name="CASE", value=ctx.channel.name, inline=True)
            embed_bunker.add_field(name="STATUS", value=status, inline=True)
            embed_bunker.add_field(name="CHARGES", value=charges, inline=False)
            embed_bunker.add_field(name="DISPOSITION", value=disposition, inline=False)
            await bunker.send(embed=embed_bunker)
        except Exception as e:
            await ctx.send(f"⚠️ Bunker Error: {e}")

    # 2. Archive Transmission
    if records:
        try:
            embed_public = discord.Embed(title="📜 EMPIRE ARCHIVE: CASE CLOSED", color=0xFFD700)
            embed_public.add_field(name="CASE", value=ctx.channel.name, inline=True)
            embed_public.add_field(name="VERDICT", value=status, inline=False)
            await records.send(embed=embed_public)
        except Exception as e:
            await ctx.send(f"⚠️ Records Error: {e}")

    # 3. Thread Closure
    try:
        await ctx.channel.edit(archived=True, locked=True)
        await ctx.send("Verdict processed. Records sealed and thread closed.")
    except Exception as e:
        await ctx.send(f"⚠️ Thread Close Error: {e}")

bot.run(os.getenv('DISCORD_TOKEN'))
