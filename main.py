import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# IDs
JUDGE_ROLE_ID = 1519179704500748388
ARCHIVIST_ROLE_ID = 1519179773602037811
trial_states = {}

@bot.command()
@commands.has_role(JUDGE_ROLE_ID)
async def trial(ctx, accuser: discord.Member, defendant: discord.Member, *, charge: str):
    declaration = (
        f"⚖️ **THE COURT OF SCARS’ EMPIRE CONVENES** ⚖️\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Today in Eternity you stand before the absolute authority of Scars’ Empire. "
        f"Justice here is swift, permanent, and without mercy.\n\n"
        f"**PRESIDING JUDGE:** {ctx.author.mention}\n"
        f"**ACCUSER:** {accuser.mention}\n"
        f"**DEFENDANT:** {defendant.mention}\n\n"
        f"**CHARGES:** {charge}\n\n"
        f"📜 **THE CODE OF CONDUCT (READ OR PERISH):** 📜\n"
        f"**1. DECORUM:** Silence is mandatory. You speak only when the Judge commands.\n"
        f"**2. CONTEMPT:** Any unauthorized interruption, disrespect, or failure to follow the Judge's phase-flow results in **Contempt**. Contempt equals automatic loss of the trial.\n"
        f"**3. REPRESENTATION:** Self-representation only. No counsel.\n"
        f"**4. EVIDENCE:** All evidence must be posted as images or links within this thread. The Archivist will verify all claims.\n"
        f"**5. THE FLOW:** The Judge will cycle through phases (!next). Follow the phase, or face the wrath of the Empire.\n\n"
        f"**The Archivist is recording your every breath. The Accuser may now present their opening statement.**"
    )
    thread = await ctx.channel.create_thread(name=f"Trial: {defendant.name}", type=discord.ChannelType.public_thread)
    await thread.send(declaration)
    await ctx.send(f"The court is in session: {thread.mention}")

@bot.command()
@commands.has_role(JUDGE_ROLE_ID)
async def next(ctx):
    thread_id = ctx.channel.id
    current_phase = trial_states.get(thread_id, "Opening Statement")
    phases = {
        "Opening Statement": "Accuser's Evidence",
        "Accuser's Evidence": "Defendant's Defense",
        "Defendant's Defense": "Closing Statements",
        "Closing Statements": "Deliberation/Verdict"
    }
    next_phase = phases.get(current_phase, "Conclusion")
    trial_states[thread_id] = next_phase
    await ctx.send(f"⚖️ **PHASE SHIFT:** The court has moved to **{next_phase}**.")

@bot.command()
@commands.has_role(JUDGE_ROLE_ID)
async def enforce(ctx, rule_number: int):
    rules = {1: "DECORUM: Silence is mandatory. You speak only when commanded.", 2: "CONTEMPT: Any breach of protocol is instant loss.", 3: "REPRESENTATION: Self-representation only.", 4: "EVIDENCE: Evidence must be in the thread.", 5: "FLOW: Follow the phase instructions."}
    await ctx.send(f"⚠️ **ENFORCEMENT:** Rule {rule_number} - {rules.get(rule_number, 'Unknown Rule')}")

@bot.command()
@commands.has_role(JUDGE_ROLE_ID)
async def contempt(ctx, member: discord.Member):
    await ctx.send(f"🔨 **CONTEMPT OF COURT!** 🔨 {member.mention} is in violation. Case forfeit.")

@bot.command()
@commands.has_role(ARCHIVIST_ROLE_ID)
async def archive(ctx):
    await ctx.channel.edit(archived=True, locked=True)
    await ctx.send("🗄️ **PROCEEDINGS SEALED.**")

bot.run(os.environ['DISCORD_TOKEN'])
