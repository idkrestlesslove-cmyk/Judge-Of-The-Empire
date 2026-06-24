import discord
from discord.ext import commands
import os

# Set up the bot with necessary permissions
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"The Scars Empire Court is now in session. Logged in as {bot.user}")

# !trial [@accuser] [@defendant] [charge]
@bot.command()
@commands.has_role("Judge Of The Empire")
async def trial(ctx, accuser: discord.Member, defendant: discord.Member, *, charge: str):
    # The intimidating, formal declaration of Scars Empire Law
    declaration = (
        f"⚖️ **THE COURT OF THE SCARS EMPIRE CONVENES** ⚖️\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"The gavel has fallen. You stand before the absolute authority of the Scars Empire. "
        f"Tremble, for justice here is swift, permanent, and without mercy.\n\n"
        f"**PRESIDING JUDGE:** {ctx.author.mention}\n"
        f"**ACCUSER:** {accuser.mention}\n"
        f"**DEFENDANT:** {defendant.mention}\n\n"
        f"**THE CHARGE:** {charge}\n\n"
        f"📜 **RULES OF PROCEEDING (READ CAREFULLY OR PERISH):** 📜\n\n"
        f"**1. ABSOLUTE DECORUM:** There will be absolutely no disrespect, insolence, or swearing in this courtroom. You speak only when spoken to.\n\n"
        f"**2. CONTEMPT IS INSTANT LOSS:** Any breach of protocol, speaking out of turn, or disrespecting the Judge or Archivist will result in immediate **Contempt of Court**. Contempt triggers an instant forfeiture of your case and maximum sentencing.\n\n"
        f"**3. REPRESENTATION:** You may represent yourself or designate counsel. Choose wisely. Your words are bound by blood. False testimony or obstruction guarantees your ruin.\n\n"
        f"**4. WITNESSES & EVIDENCE:** You may not interrupt. Witnesses will only speak when formally summoned by the Judge. All documentation and evidence must be submitted directly to the thread for the Archivist's strict verification. Unverified claims are worthless.\n\n"
        f"**5. UNAUTHORIZED INTERFERENCE:** Only the Judge, Archivist, Accuser, Defendant, and summoned witnesses may speak in this thread. All outsiders who interfere will face the wrath of the Empire.\n\n"
        f"**The Archivist is now recording every breath.** The Accuser may present their opening statement."
    )
    
    # Create the thread
    thread = await ctx.channel.create_thread(
        name=f"Trial: {defendant.name} - {charge[:15]}", 
        type=discord.ChannelType.public_thread
    )
    
    # Send the formal opening into the thread
    await thread.send(declaration)
    await ctx.send(f"The Judge has called court into session. The fate of {defendant.mention} will be decided here: {thread.mention}")

# Error handling if a non-judge tries to start a trial
@trial.error
async def trial_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("Silence. Only a recognized **Judge Of The Empire** may convene a trial.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Improper formatting. Use: `!trial @Accuser @Defendant The Charge`")

# !contempt [@user] (Allows the judge to instantly end someone's case)
@bot.command()
@commands.has_role("Judge Of The Empire")
async def contempt(ctx, member: discord.Member):
    await ctx.send(f"🔨 **CONTEMPT OF COURT!** 🔨\n"
                   f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                   f"{member.mention} has violated the sacred rules of the Scars Empire Court. "
                   f"By the absolute power of the Judge, this case is instantly forfeit against the offender. "
                   f"Prepare for immediate sentencing.")

# Error handling for contempt
@contempt.error
async def contempt_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("Only a **Judge Of The Empire** may strike a soul with contempt.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Specify who is in contempt. Use: `!contempt @User`")

# !archive (Closes and locks the thread, only for the Archivist)
@bot.command()
@commands.has_role("Archivist")
async def archive(ctx):
    # Ensure this command is only used inside a thread
    if isinstance(ctx.channel, discord.Thread):
        await ctx.send("🗄️ **PROCEEDINGS CONCLUDED.**\n"
                       "The evidence phase is over. The Archivist has verified the Dossier. "
                       "The record is now permanent and this thread shall be locked. May the Empire have mercy.")
        # Locks the thread so no one else can type in it
        await ctx.channel.edit(archived=True, locked=True)
    else:
        await ctx.send("This command can only be used to seal an active trial thread.")

# Error handling for archive
@archive.error
async def archive_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("Do not touch the royal records. Only an **Archivist** may seal a dossier.")

bot.run(os.environ['DISCORD_TOKEN'])
