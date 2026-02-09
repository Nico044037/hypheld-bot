import os
import discord
from discord.ext import commands

# ===== CONFIG =====
GUILD_ID = 1452967364470505565
TOKEN = os.getenv("MTQ3MDQ2NDg2MzIzODM1NzA5Mw.G4p-fF.QrRWHDocHp9m0by8DitI3bXluocEnmyv0HMu-4")

# ===== INTENTS =====
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def send(ctx):
    # Only allow in the correct server
    if ctx.guild is None or ctx.guild.id != GUILD_ID:
        return

    embed = discord.Embed(
        title="📜 WELCOME TO THE RULES",
        description="Please read carefully to keep **Hypheld** fun and fair ❤️",
        color=discord.Color.red()
    )

    embed.add_field(
        name="💬 Discord Rules",
        value=(
            "🤝 Be respectful to everyone\n"
            "🚫 No spamming or excessive tagging\n"
            "🔞 No NSFW or disturbing content\n"
            "📢 No advertising without staff permission\n"
            "⚠️ No illegal activity\n"
            "🔐 Do not share personal information\n"
            "🧭 Use the correct channels\n"
            "👮 Staff decisions are final"
        ),
        inline=False
    )

    embed.add_field(
        name="🎮 Minecraft Server Rules",
        value=(
            "❌ No hacking, x-ray, or cheats\n"
            "🐞 No exploiting bugs or glitches\n"
            "💬 No toxic behavior\n"
            "👤 No alt accounts without approval\n"
            "💸 No scamming or real-money trading\n"
            "📕 Follow Minecraft’s EULA"
        ),
        inline=False
    )

    embed.set_footer(text="⚠️ Breaking rules may result in mutes, bans, or wipes")

    await ctx.send(embed=embed)

# ===== START BOT =====
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable not set")

bot.run(TOKEN)
