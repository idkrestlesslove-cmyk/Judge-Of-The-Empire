import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- REPLACE THESE NUMBERS WITH YOUR ACTUAL ROLE IDS ---
# Right-click your role in Server Settings > Roles and "Copy Role ID"
JUDGE_ROLE_ID = 123456789012345678 
ARCHIVIST_ROLE_ID = 123456789012345678
# -------------------------------------------------------

@bot.event
async def on_ready():
    print(f"The Scars Empire Court is now in session. Logged in as {bot.user}")

@bot.command()
@commands.has_role(JUDGE_ROLE_ID)
async def trial(ctx, accuser: discord.Member, defendant: discord.Member, *, charge: str):
    # The updated Scars' Empire declaration
    declaration = (
        f"⚖️ **THE COURT OF SCARS’ EMPIRE CONVENES** ⚖️\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Today in Eternity you stand before the absolute authority of Scars’ Empire. "
        f"Justice here is swift, permanent, and without mercy.\n\n"
        f"**PRESIDING JUDGE:** {ctx.author.mention}\n"
        f"**ACCUSER:** {accuser.mention}\n"
        f"**DEFENDANT:** {defendant.mention}\n\n"
        f"**Charges:** {charge}\n\n"
        f"📜 **RULES OF PROCEEDING (READ CAREFULLY OR PERISH):** 📜\n\n"
        f"**1. ABSOLUTE DECORUM:** There will be absolutely no disrespect, insolence, or swearing in this courtroom. You speak only when spoken to.\n\n"
        f"**2. CONTEMPT IS INSTANT LOSS:** Any multiple violations at judges discretion for breach of protocol, speaking out of turn, or disrespecting the Judge or The Empire will result in immediate **Contempt of Court**. Contempt triggers an instant forfeiture of your case and a proceeding with the maximum sentencing.\n\n"
        f"**3. REPRESENTATION:** You may only represent yourself. False testimony or obstruction guarantees your ruin.\n\n"
        f"**4. WITNESSES & EVIDENCE:** You may not interrupt. Witnesses will only speak if formally summoned by the Judge. All documentation and evidence must be submitted directly to the thread for the Archivist's strict verification. Unverified claims are worthless.\n\n"
        f"**5. UNAUTHORIZED INTERFERENCE:** Only the Judge, Archivist, Accuser, Defendant, and summoned witnesses may speak in this thread. All outsiders who interfere will face the wrath of the Empire.\n\n"
        f"**The Archivist is now recording your every breath.** The Accuser may present their opening statement."
    )
    
    # Create the thread
    thread = await ctx.channel.create_thread(
        name=f"Trial: {defendant.name}", 
        type=discord.ChannelType.public_thread
    )
    
    # Send the formal opening into the thread
    await thread.send(declaration)
    await ctx.send(f"The Judge has called court into session. The fate of {defendant.mention} will be decided here: {thread.mention}")

@trial.error
async def trial_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("Silence. Only a recognized **Judge Of The Empire** may convene a trial.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Improper formatting. Use: `!trial @Accuser @Defendant The Charge`")

@bot.command()
@commands.has_role(JUDGE_ROLE_ID)
async def contempt(ctx, member: discord.Member):
    await ctx.send(f"🔨 **CONTEMPT OF COURT!** 🔨\n"
                   f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                   f"{member.mention} has violated the sacred rules of the Scars Empire Court. "
                   f"This case is instantly forfeit. Prepare for immediate sentencing.")

@bot.command()
@commands.has_role(ARCHIVIST_ROLE_ID)
async def archive(ctx):
    if isinstance(ctx.channel, discord.Thread):
        await ctx.send("🗄️ **PROCEEDINGS CONCLUDED.**\n"
                       "The evidence phase is over. The record is now permanent and this thread shall be locked. May the Empire have mercy.")
        await ctx.channel.edit(archived=True, locked=True)
    else:
        await ctx.send("This command can only be used to seal an active trial thread.")

bot.run(os.environ['DISCORD_TOKEN'])
