import os
import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.getenv("MTQ3MDQ2NDg2MzIzODM1NzA5Mw.G4p-fF.QrRWHDocHp9m0by8DitI3bXluocEnmyv0HMu-4")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    # Sync slash commands globally
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")
    print("✅ Slash commands synced")

# ===== SLASH COMMAND =====
@bot.tree.command(name="send", description="Send the server rules")
async def send(interaction: discord.Interaction):
    # Prevent DMs
    if interaction.guild is None:
        await interaction.response.send_message(
            "❌ This command can only be used in a server.",
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title="📜 WELCOME TO THE RULES",
        description="Please read carefully to keep the server fun and fair ❤️",
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

    await interaction.response.send_message(embed=embed)

# ===== START BOT =====
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable not set")

bot.run(TOKEN)
