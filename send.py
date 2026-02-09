import discord
from discord.ext import commands

TOKEN = "MTQ3MDQ2NDg2MzIzODM1NzA5Mw.G4p-fF.QrRWHDocHp9m0by8DitI3bXluocEnmyv0HMu-4"
ALLOWED_GUILD_ID = 1452967364470505565

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def send(ctx):
    # Check if command is used in the correct server
    if ctx.guild is None or ctx.guild.id != ALLOWED_GUILD_ID:
        return

    embed = discord.Embed(
        title="📜 WELCOME TO THE RULES",
        description="Please read carefully to keep **Hypheld** fun and fair ❤️",
        color=discord.Color.dark_red()
    )

    embed.add_field(
        name="💬 Discord Rules",
        value=(
            "🤝 Be respectful to everyone — no harassment, hate speech, or bullying.\n"
            "🚫 No spamming, flooding, or excessive tagging.\n"
            "🔞 No NSFW, gore, or disturbing content.\n"
            "📢 No advertising without staff permission.\n"
            "⚠️ No illegal activity or harmful links.\n"
            "🔐 Do not share personal information.\n"
            "🧭 Use the correct channels.\n"
            "📜 Follow Discord TOS & Guidelines.\n"
            "👮 Staff decisions are final — open a ticket if needed."
        ),
        inline=False
    )

    embed.add_field(
        name="🎮 Minecraft Server Rules",
        value=(
            "❌ No hacking, x-ray, cheats, or unfair mods.\n"
            "🐞 No bug or glitch abusing.\n"
            "💬 No toxic behavior (chat or Discord).\n"
            "👤 No alt accounts without approval.\n"
            "💸 No scamming or real-money trading.\n"
            "📕 Follow Minecraft’s EULA."
        ),
        inline=False
    )

    embed.set_footer(text="⚠️ Breaking rules may result in mutes, bans, or wipes")

    await ctx.send(embed=embed)

bot.run(TOKEN)
