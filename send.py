import os
import json
import asyncio
import discord
import aiohttp
from datetime import datetime
from discord.ext import commands

# ================= BASIC CONFIG =================
TOKEN = os.getenv("DISCORD_TOKEN")
MAIN_GUILD_ID = int(os.getenv("GUILD_ID", "1452967364470505565"))
DATA_FILE = "data.json"

OWNER_ID = 1265323465079259166

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix=["!", "?", "$"],
    intents=intents,
    help_command=None
)

# ================= FORCE COMMAND PROCESSING =================
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

# ================= STORAGE =================
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"welcome_channel": None, "autoroles": []}, f)

with open(DATA_FILE, "r") as f:
    data = json.load(f)

welcome_channel_id = data.get("welcome_channel")
autoroles = set(data.get("autoroles", []))


def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(
            {
                "welcome_channel": welcome_channel_id,
                "autoroles": list(autoroles)
            },
            f,
            indent=4
        )

# ================= EMBEDS =================
def rules_embed():
    embed = discord.Embed(
        title="📜 Welcome to the Server!",
        description="Please read the rules carefully ❤️",
        color=discord.Color.red()
    )

    embed.add_field(
        name="💬 Discord Rules",
        value=(
            "🤝 Be respectful\n"
            "🚫 No spamming\n"
            "🔞 No NSFW\n"
            "📢 No advertising\n"
            "⚠️ No illegal content\n"
            "👮 Staff decisions are final"
        ),
        inline=False
    )

    embed.set_footer(text="⚠️ Breaking rules may result in punishment")
    return embed

# ================= READY =================
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# ================= MEMBER JOIN =================
@bot.event
async def on_member_join(member: discord.Member):
    if member.guild.id != MAIN_GUILD_ID:
        return

    await asyncio.sleep(2)

    try:
        await member.send(embed=rules_embed())
    except:
        pass

    if autoroles:
        roles_to_add = []
        for role_id in autoroles:
            role = member.guild.get_role(role_id)
            if role and not role.managed and role < member.guild.me.top_role:
                roles_to_add.append(role)

        if roles_to_add:
            try:
                await member.add_roles(*roles_to_add, reason="Autorole")
            except:
                pass

    if welcome_channel_id:
        channel = member.guild.get_channel(welcome_channel_id)
        if channel:
            await channel.send(
                f"👋 Welcome {member.mention}!\n📜 Check your DMs ❤️"
            )

# ================= SETUP =================
@bot.command()
@commands.has_permissions(manage_guild=True)
async def setup(ctx, channel: discord.TextChannel):
    global welcome_channel_id
    welcome_channel_id = channel.id
    save_data()
    await ctx.send(f"✅ Welcome channel set to {channel.mention}")

# ================= SEND RULES =================
@bot.command()
async def send(ctx):
    await ctx.send(embed=rules_embed())

# ================= HELP =================
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="📖 Help Menu",
        description="All available commands",
        color=discord.Color.blurple()
    )

    embed.add_field(name="⚙️ Setup", value="`!setup #channel`", inline=False)
    embed.add_field(
        name="🏷️ Autorole",
        value="`?autorole add @role`\n`?autorole remove @role`",
        inline=False
    )
    embed.add_field(name="📜 Rules", value="`!send`", inline=False)
    embed.add_field(
        name="🔨 Moderation",
        value="`?kick @user [reason]`\n`?role add/remove @user @role`",
        inline=False
    )
    embed.add_field(
        name="🔥 Owner",
        value="`$sudo info <mc_username>`",
        inline=False
    )

    await ctx.send(embed=embed)

# ================= MODERATION =================
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"👢 Kicked {member.mention}")
    except:
        await ctx.send("❌ Cannot kick this user.")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def role(ctx, action: str, member: discord.Member, role: discord.Role):
    if role >= ctx.guild.me.top_role:
        return await ctx.send("❌ Role above my highest role.")

    if action.lower() == "add":
        await member.add_roles(role)
        await ctx.send(f"✅ Added {role.mention}")
    elif action.lower() == "remove":
        await member.remove_roles(role)
        await ctx.send(f"❌ Removed {role.mention}")

# ================= AUTOROLE =================
@bot.command()
@commands.has_permissions(manage_roles=True)
async def autorole(ctx, action: str, role: discord.Role):
    if role >= ctx.guild.me.top_role:
        return await ctx.send("❌ Role too high.")

    if action.lower() == "add":
        autoroles.add(role.id)
        save_data()
        await ctx.send("✅ Autorole added")
    elif action.lower() == "remove":
        autoroles.discard(role.id)
        save_data()
        await ctx.send("❌ Autorole removed")

# ================= SUDO GROUP =================
@bot.group(name="sudo")
async def sudo(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("⚠️ Subcommands: info")

# ================= SUDO INFO =================
@sudo.command(name="info")
@commands.has_permissions(administrator=True)
async def sudo_info(ctx, mc_username: str):

    await ctx.send("🔎 Fetching Minecraft data...")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.mojang.com/users/profiles/minecraft/{mc_username}"
            ) as response:

                if response.status != 200:
                    return await ctx.send(
                        f"❌ No Minecraft account found for `{mc_username}`."
                    )

                data = await response.json()
                uuid_raw = data["id"]

        uuid = (
            f"{uuid_raw[:8]}-{uuid_raw[8:12]}-"
            f"{uuid_raw[12:16]}-{uuid_raw[16:20]}-{uuid_raw[20:]}"
        )

        embed = discord.Embed(
            title="🎮 Minecraft Account Info",
            color=discord.Color.green()
        )

        embed.add_field(name="Username", value=mc_username, inline=False)
        embed.add_field(name="UUID", value=uuid, inline=False)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ Unexpected error: `{str(e)}`")

# ================= START =================
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN not set")

bot.run(TOKEN)