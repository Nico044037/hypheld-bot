# ===== HELP COMMAND (?help / !help) =====
@bot.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(
        title="📖 Bot Help Menu",
        description="Dyno-style commands for this server",
        color=discord.Color.blurple()
    )

    embed.add_field(
        name="⚙️ Setup",
        value=(
            "`/setup #channel`\n"
            "`!setup #channel`\n"
            "`?setup #channel`"
        ),
        inline=False
    )

    embed.add_field(
        name="📜 Rules",
        value=(
            "`/send`\n"
            "`!send`\n"
            "`?send`"
        ),
        inline=False
    )

    embed.add_field(
        name="🔨 Moderation",
        value=(
            "`?kick @user [reason]`\n"
            "`?role add @user @role`\n"
            "`?role remove @user @role`"
        ),
        inline=False
    )

    embed.set_footer(text="Only staff can use moderation commands")
    await ctx.send(embed=embed)
