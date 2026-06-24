import discord
from discord.ext import commands
import os

# Set up the bot with necessary permissions
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Empire Clerk online as {bot.user}")

# !accuse [mention_user] [charge]
@bot.command()
async def accuse(ctx, member: discord.Member, *, charge: str):
    # Create a private thread for the case
    thread = await ctx.channel.create_thread(
        name=f"Case: {member.name}", 
        type=discord.ChannelType.public_thread
    )
    await thread.send(f"**OFFICIAL CASE FILE**\nDefendant: {member.mention}\nCharge: {charge}\n\n"
                      "Procedures: \n1. Accuser: Submit evidence below.\n"
                      "2. Defendant: Submit rebuttal below.\n"
                      "3. Archivist: Type '!finalize' when evidence is complete.")
    await ctx.send(f"Trial initiated in {thread.mention}")

# !finalize (This closes the argument and prepares the dossier)
@bot.command()
async def finalize(ctx):
    await ctx.send("**Evidence phase concluded.** The Archivist has verified the Dossier. "
                   "Jury, please review the thread above and submit your verdict via DM.")

bot.run(os.environ['DISCORD_TOKEN'])
