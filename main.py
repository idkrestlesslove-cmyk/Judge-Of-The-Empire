import discord
from discord.ext import commands
import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

case_counter = 100 # Starting case number
JUDGE_ROLE_ID = 1519179704500748388
ARCHIVIST_ROLE_ID = 1519179773602037811
VAULT_CHANNEL_ID = 000000000000000000 # Add your Vault Channel ID
RECORDS_CHANNEL_ID = 000000000000000000 # Add your Records Channel ID

# EMBED COLORS
BLACK = 0x000000
GOLD = 0xFFD700
WHITE = 0xFFFFFF

@bot.command()
@commands.has_role(JUDGE_ROLE_ID)
async def trial(ctx, defendant: discord.Member, *, charge: str):
    global case_counter
    case_counter += 1
    case_num = f"CASE-{case_counter}"
    
    embed = discord.Embed(title="⚖️ COURT OF THE EMPIRE: SESSION OPENED", color=WHITE)
    embed.add_field(name="CASE NUMBER", value=case_num, inline=True)
    embed.add_field(name="DEFENDANT", value=defendant.mention, inline=True)
    embed.add_field(name="CHARGE", value=charge, inline=False)
    embed.set_footer(text="Proceedings are classified until verdict.")
    
    thread = await ctx.channel.create_thread(name=f"{case_num} | {defendant.name}", type=discord.ChannelType.private_thread)
    await thread.send(embed=embed)
    await ctx.send(f"**{case_num}** has been registered. The court is in session.")

@bot.command()
@commands.has_role(JUDGE_ROLE_ID)
async def verdict(ctx, charges: str, status: str, *, disposition: str):
    vault = bot.get_channel(VAULT_CHANNEL_ID)
    records = bot.get_channel(RECORDS_CHANNEL_ID)
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

bot.run(os.environ['DISCORD_TOKEN'])
