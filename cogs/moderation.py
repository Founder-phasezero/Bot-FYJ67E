import discord
from discord.ext import commands
from datetime import timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 1 — Kick
    @commands.command(name="kick")
    @commands.has_guild_permissions(kick_members=True)
    async def mod_kick(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        await member.kick(reason=reason)
        await ctx.send(f"👢 Kicked **{member}** — {reason}")

    # 2 — Ban
    @commands.command(name="ban")
    @commands.has_guild_permissions(ban_members=True)
    async def mod_ban(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 Banned **{member}** — {reason}")

    # 3 — Unban
    @commands.command(name="unban")
    @commands.has_guild_permissions(ban_members=True)
    async def mod_unban(self, ctx, user: discord.User):
        await ctx.guild.unban(user)
        await ctx.send(f"♻️ Unbanned **{user}**")

    # 4 — Timeout
    @commands.command(name="timeout")
    @commands.has_guild_permissions(moderate_members=True)
    async def mod_timeout(self, ctx, member: discord.Member, minutes: int):
        duration = timedelta(minutes=minutes)
        await member.timeout(duration)
        await ctx.send(f"⏳ Timed out **{member}** for **{minutes} minutes**")

    # 5 — Remove Timeout
    @commands.command(name="untimeout")
    @commands.has_guild_permissions(moderate_members=True)
    async def mod_untimeout(self, ctx, member: discord.Member):
        await member.timeout(None)
        await ctx.send(f"✅ Removed timeout for **{member}**")

    # 6 — Purge messages
    @commands.command(name="purge")
    @commands.has_guild_permissions(manage_messages=True)
    async def mod_purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"🧹 Deleted **{amount} messages**", delete_after=5)

    # 7 — Lock channel
    @commands.command(name="lock")
    @commands.has_guild_permissions(manage_channels=True)
    async def mod_lock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("🔒 Channel locked.")

    # 8 — Unlock channel
    @commands.command(name="unlock")
    @commands.has_guild_permissions(manage_channels=True)
    async def mod_unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("🔓 Channel unlocked.")

    # 9 — Slowmode
    @commands.command(name="slowmode")
    @commands.has_guild_permissions(manage_channels=True)
    async def mod_slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"🐌 Slowmode set to **{seconds}s**")

    # 10 — Disable slowmode
    @commands.command(name="unslowmode")
    @commands.has_guild_permissions(manage_channels=True)
    async def mod_unslowmode(self, ctx):
        await ctx.channel.edit(slowmode_delay=0)
        await ctx.send("🐌 Slowmode disabled.")

    # 11 — Warn
    @commands.command(name="warn")
    @commands.has_guild_permissions(manage_messages=True)
    async def mod_warn(self, ctx, member: discord.Member, *, reason: str):
        await ctx.send(f"⚠️ **{member}** has been warned: {reason}")

    # 12 — Mute
    @commands.command(name="mute")
    @commands.has_guild_permissions(moderate_members=True)
    async def mod_mute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(role, send_messages=False)
        await member.add_roles(role)
        await ctx.send(f"🔇 Muted **{member}**")

    # 13 — Unmute
    @commands.command(name="unmute")
    @commands.has_guild_permissions(moderate_members=True)
    async def mod_unmute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if role:
            await member.remove_roles(role)
        await ctx.send(f"🔊 Unmuted **{member}**")

    # 14 — Change nickname
    @commands.command(name="nick")
    @commands.has_guild_permissions(manage_nicknames=True)
    async def mod_nick(self, ctx, member: discord.Member, *, nickname: str):
        await member.edit(nick=nickname)
        await ctx.send(f"✏️ Nickname changed to **{nickname}**")

    # 15 — Reset nickname
    @commands.command(name="resetnick")
    @commands.has_guild_permissions(manage_nicknames=True)
    async def mod_resetnick(self, ctx, member: discord.Member):
        await member.edit(nick=None)
        await ctx.send(f"♻️ Reset nickname for **{member}**")

    # 16 — Server stats
    @commands.command(name="stats")
    @commands.has_guild_permissions(manage_guild=True)
    async def mod_stats(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title="📊 Server Moderation Stats", color=discord.Color.orange())
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name="Channels", value=len(guild.channels))
        embed.add_field(name="Roles", value=len(guild.roles))
        await ctx.send(embed=embed)

    # 17 — Role add
    @commands.command(name="roleadd")
    @commands.has_guild_permissions(manage_roles=True)
    async def mod_roleadd(self, ctx, member: discord.Member, role: discord.Role):
        await member.add_roles(role)
        await ctx.send(f"➕ Added role **{role.name}** to **{member}**")

    # 18 — Role remove
    @commands.command(name="roleremove")
    @commands.has_guild_permissions(manage_roles=True)
    async def mod_roleremove(self, ctx, member: discord.Member, role: discord.Role):
        await member.remove_roles(role)
        await ctx.send(f"➖ Removed role **{role.name}** from **{member}**")

    # 19 — Channel info
    @commands.command(name="channelinfo")
    async def mod_channelinfo(self, ctx):
        channel = ctx.channel
        embed = discord.Embed(title="ℹ️ Channel Info", color=discord.Color.blue())
        embed.add_field(name="Name", value=channel.name)
        embed.add_field(name="ID", value=channel.id)
        embed.add_field(name="Slowmode", value=channel.slowmode_delay)
        await ctx.send(embed=embed)

    # 20 — Server info (rename to avoid conflicts)
    @commands.command(name="modserverinfo")
    async def mod_serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title="🛡️ Server Info", color=discord.Color.dark_teal())
        embed.add_field(name="Name", value=guild.name)
        embed.add_field(name="Owner", value=guild.owner)
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d"))
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
