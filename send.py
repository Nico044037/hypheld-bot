import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 1452967364470505565

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== CONFIG (set by !setup) =====
welcome_channel_id: int | None = None

# ===== RULES EMBED =====
def rules_embed():
    embed = discord.Embed(
        title="📜 Welcome to the Server!",
        description="Please read the rules carefully ❤️",
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

# ===== READY =====
@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync(guild=guild)
    print(f"✅ Logged in as {bot.user}")

# ===== MEMBER JOIN (DM + WELCOME) =====
@bot.event
async def on_member_join(member: discord.Member):
    if member.guild.id != GUILD_ID:
        return

    # DM rules
    try:
        await member.send(embed=rules_embed())
    except discord.Forbidden:
        pass

    # Welcome message
    if welcome_channel_id:
        channel = bot.get_channel(welcome_channel_id)
        if channel:
            await channel.send(
                f"👋 Welcome {member.mention}!\n"
                f"📜 Please check your DMs for the rules ❤️"
            )

# ===== !SETUP COMMAND =====
@bot.command()
@commands.has_permissions(manage_guild=True)
async def setup(ctx, channel: discord.TextChannel):
    global welcome_channel_id

    if ctx.guild.id != GUILD_ID:
        return

    welcome_channel_id = channel.id

    await ctx.send(
        f"✅ **Setup complete!**\n"
        f"📌 Welcome channel set to {channel.mention}\n"
        f"📨 New members will now receive rules in DMs."
    )

@setup.error
async def setup_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need **Manage Server** permission to use this.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Please mention a channel. Example: `!setup #welcome`")

# ===== SLASH COMMAND =====
@bot.tree.command(name="send", description="Send the server rules")
async def slash_send(interaction: discord.Interaction):
    await interaction.response.send_message(embed=rules_embed())

# ===== PREFIX COMMAND =====
@bot.command()
async def send(ctx):
    await ctx.send(embed=rules_embed())

# ===== START =====
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable not set")

bot.run(TOKEN)
