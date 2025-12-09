import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ---------------- PREFIX COMMANDS ----------------

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        try:
            await member.kick(reason=reason)
            await ctx.send(f"✅ {member.mention} has been kicked. Reason: {reason}")
        except Exception as e:
            await ctx.send(f"❌ Could not kick {member.mention}: {e}")

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        try:
            await member.ban(reason=reason)
            await ctx.send(f"✅ {member.mention} has been banned. Reason: {reason}")
        except Exception as e:
            await ctx.send(f"❌ Could not ban {member.mention}: {e}")

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int):
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user)
            await ctx.send(f"✅ Unbanned {user}.")
        except Exception as e:
            await ctx.send(f"❌ Could not unban user: {e}")

    @commands.command(name="mute")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason: str = None):
        try:
            mute_role = discord.utils.get(ctx.guild.roles, name="Muted-by-PhaseZero")
            if not mute_role:
                mute_role = await ctx.guild.create_role(name="Muted-by-PhaseZero")
                for channel in ctx.guild.channels:
                    await channel.set_permissions(mute_role, speak=False, send_messages=False)
            await member.add_roles(mute_role, reason=reason)
            await ctx.send(f"✅ {member.mention} has been muted.")
        except Exception as e:
            await ctx.send(f"❌ Could not mute {member.mention}: {e}")

    @commands.command(name="unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        try:
            mute_role = discord.utils.get(ctx.guild.roles, name="Muted-by-PhaseZero")
            if mute_role:
                await member.remove_roles(mute_role)
                await ctx.send(f"✅ {member.mention} has been unmuted.")
            else:
                await ctx.send("❌ Mute role not found.")
        except Exception as e:
            await ctx.send(f"❌ Could not unmute {member.mention}: {e}")

    @commands.command(name="slowmode")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"✅ Slowmode set to {seconds} seconds.")

    @commands.command(name="lockdown")
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send("🔒 Channel is now in lockdown.")

    @commands.command(name="unlock")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send("🔓 Channel unlocked.")

    @commands.command(name="prune")
    @commands.has_permissions(manage_messages=True)
    async def prune(self, ctx, amount: int):
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"🗑️ Deleted {len(deleted)} messages.", delete_after=5)

    @commands.command(name="announce")
    @commands.has_permissions(manage_messages=True)
    async def announce(self, ctx, *, message: str):
        await ctx.send(f"📢 {message}")

    @commands.command(name="renamechannel")
    @commands.has_permissions(manage_channels=True)
    async def renamechannel(self, ctx, *, new_name: str):
        await ctx.channel.edit(name=new_name)
        await ctx.send(f"✅ Channel renamed to {new_name}.")

    @commands.command(name="roleadd")
    @commands.has_permissions(manage_roles=True)
    async def roleadd(self, ctx, member: discord.Member, role: discord.Role):
        await member.add_roles(role)
        await ctx.send(f"✅ Added {role.name} to {member.mention}.")

    @commands.command(name="roleremove")
    @commands.has_permissions(manage_roles=True)
    async def roleremove(self, ctx, member: discord.Member, role: discord.Role):
        await member.remove_roles(role)
        await ctx.send(f"✅ Removed {role.name} from {member.mention}.")

    @commands.command(name="channelcreate")
    @commands.has_permissions(manage_channels=True)
    async def channelcreate(self, ctx, *, name: str):
        await ctx.guild.create_text_channel(name)
        await ctx.send(f"✅ Channel '{name}' created.")

    @commands.command(name="channeldelete")
    @commands.has_permissions(manage_channels=True)
    async def channeldelete(self, ctx, channel: discord.TextChannel):
        await channel.delete()
        await ctx.send(f"🗑️ Channel {channel.name} deleted.")

    @commands.command(name="purgeuser")
    @commands.has_permissions(manage_messages=True)
    async def purgeuser(self, ctx, member: discord.Member, limit: int = 100):
        def is_user(m):
            return m.author == member
        deleted = await ctx.channel.purge(limit=limit, check=is_user)
        await ctx.send(f"🗑️ Deleted {len(deleted)} messages from {member.mention}.", delete_after=5)

async def setup(bot):
    await bot.add_cog(Admin(bot))
