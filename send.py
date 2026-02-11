import os
import json
import asyncio
import discord
import aiohttp
from datetime import datetime
from discord import app_commands

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", "1452967364470505565"))
DATA_FILE = "data.json"

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

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

# ================= READY =================
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"✅ Logged in as {client.user}")

# ================= MEMBER JOIN =================
@client.event
async def on_member_join(member):
    if member.guild.id != GUILD_ID:
        return

    await asyncio.sleep(2)

    if autoroles:
        roles_to_add = []
        for role_id in autoroles:
            role = member.guild.get_role(role_id)
            if role and role < member.guild.me.top_role:
                roles_to_add.append(role)

        if roles_to_add:
            await member.add_roles(*roles_to_add)

    if welcome_channel_id:
        channel = member.guild.get_channel(welcome_channel_id)
        if channel:
            await channel.send(f"👋 Welcome {member.mention}!")

# ================= BASIC =================
@tree.command(name="ping", description="Test if bot works", guild=discord.Object(id=GUILD_ID))
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")

@tree.command(name="send", description="Send rules embed", guild=discord.Object(id=GUILD_ID))
async def send(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📜 Server Rules",
        description="Please follow the rules ❤️",
        color=discord.Color.red()
    )
    embed.add_field(
        name="Rules",
        value="Be respectful\nNo spam\nNo NSFW\nNo advertising",
        inline=False
    )
    await interaction.response.send_message(embed=embed)

# ================= SETUP =================
@tree.command(name="setup", description="Set welcome channel", guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(manage_guild=True)
async def setup(interaction: discord.Interaction, channel: discord.TextChannel):
    global welcome_channel_id
    welcome_channel_id = channel.id
    save_data()
    await interaction.response.send_message(f"✅ Welcome channel set to {channel.mention}")

# ================= AUTOROLE =================
@tree.command(name="autorole", description="Add or remove autorole", guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(manage_roles=True)
async def autorole(interaction: discord.Interaction, action: str, role: discord.Role):
    if role >= interaction.guild.me.top_role:
        return await interaction.response.send_message("❌ Role too high.", ephemeral=True)

    if action.lower() == "add":
        autoroles.add(role.id)
        save_data()
        await interaction.response.send_message("✅ Autorole added")
    elif action.lower() == "remove":
        autoroles.discard(role.id)
        save_data()
        await interaction.response.send_message("❌ Autorole removed")
    else:
        await interaction.response.send_message("Use add or remove.", ephemeral=True)

# ================= KICK =================
@tree.command(name="kick", description="Kick a member", guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason"):
    try:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"👢 Kicked {member.mention}")
    except:
        await interaction.response.send_message("❌ Cannot kick this user.", ephemeral=True)

# ================= ROLE =================
@tree.command(name="role", description="Add or remove role", guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(manage_roles=True)
async def role(interaction: discord.Interaction, action: str, member: discord.Member, role: discord.Role):
    if role >= interaction.guild.me.top_role:
        return await interaction.response.send_message("❌ Role too high.", ephemeral=True)

    if action.lower() == "add":
        await member.add_roles(role)
        await interaction.response.send_message(f"✅ Added {role.mention}")
    elif action.lower() == "remove":
        await member.remove_roles(role)
        await interaction.response.send_message(f"❌ Removed {role.mention}")
    else:
        await interaction.response.send_message("Use add or remove.", ephemeral=True)

# ================= SUDO INFO =================
@tree.command(name="sudo_info", description="Minecraft lookup", guild=discord.Object(id=GUILD_ID))
@app_commands.checks.has_permissions(administrator=True)
async def sudo_info(interaction: discord.Interaction, mc_username: str):

    await interaction.response.defer()

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.mojang.com/users/profiles/minecraft/{mc_username}"
            ) as response:

                if response.status != 200:
                    return await interaction.followup.send("❌ Account not found.")

                data = await response.json()
                uuid_raw = data["id"]

        uuid = (
            f"{uuid_raw[:8]}-{uuid_raw[8:12]}-"
            f"{uuid_raw[12:16]}-{uuid_raw[16:20]}-{uuid_raw[20:]}"
        )

        embed = discord.Embed(title="Minecraft Info", color=discord.Color.green())
        embed.add_field(name="Username", value=mc_username)
        embed.add_field(name="UUID", value=uuid)

        await interaction.followup.send(embed=embed)

    except Exception as e:
        await interaction.followup.send(f"❌ Error: {e}")

# ================= START =================
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN not set")

client.run(TOKEN)