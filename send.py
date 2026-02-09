import os
import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 1452967364470505565

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== READY EVENT =====
@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)

    # Instant guild sync
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)

    print(f"✅ Logged in as {bot.user}")
    print(f"✅ Slash commands synced to guild {GUILD_ID}")

# ===== EMBED BUILDER =====
def rules_embed():
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
    return embed

# ===== SLASH COMMAND =====
@bot.tree.command(name="send", description="Send the server rules")
async def slash_send(interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message(
            "❌ This command can only be used in a server.",
            ephemeral=True
        )
        return

    await interaction.response.send_message(embed=rules_embed())

# ===== PREFIX COMMAND =====
@bot.command()
async def send(ctx):
    if ctx.guild is None:
        return

    await ctx.send(embed=rules_embed())

# ===== START BOT =====
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable not set")

bot.run(TOKEN)


