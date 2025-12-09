import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ---------------- PREFIX COMMANDS ----------------

    @commands.command(name="hello")
    async def hello(self, ctx):
        await ctx.send(f"Hello {ctx.author.mention}! 👋")

    @commands.command(name="userinfo")
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"User Info: {member}", color=discord.Color.blurple())
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Top Role", value=member.top_role, inline=True)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime('%Y-%m-%d'), inline=True)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else discord.Embed.Empty)
        await ctx.send(embed=embed)

    @commands.command(name="serverinfo2")
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"Server Info: {guild.name}", color=discord.Color.green())
        embed.add_field(name="Server ID", value=guild.id)
        embed.add_field(name="Owner", value=guild.owner)
        embed.add_field(name="Members", value=guild.member_count)
        embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)
        await ctx.send(embed=embed)

    @commands.command(name="avatar")
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"Avatar for {member}", color=discord.Color.purple())
        embed.set_image(url=member.avatar.url if member.avatar else discord.Embed.Empty)
        await ctx.send(embed=embed)

    @commands.command(name="say")
    async def say(self, ctx, *, message: str):
        await ctx.send(message)

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send(f"Pong! {self.bot.latency*1000:.2f}ms")

    @commands.command(name="uptime")
    async def uptime(self, ctx):
        import time
        delta = time.time() - self.bot.uptime
        hours, remainder = divmod(int(delta), 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.send(f"Uptime: {hours}h {minutes}m {seconds}s")

    @commands.command(name="roles")
    async def roles(self, ctx):
        roles = [role.name for role in ctx.author.roles if role.name != "@everyone"]
        await ctx.send(f"Your roles: {', '.join(roles)}")

    @commands.command(name="servericon")
    async def servericon(self, ctx):
        guild = ctx.guild
        if guild.icon:
            await ctx.send(guild.icon.url)
        else:
            await ctx.send("Server has no icon.")

    @commands.command(name="members")
    async def members(self, ctx):
        await ctx.send(f"Server has {ctx.guild.member_count} members.")

    @commands.command(name="rolescount")
    async def rolescount(self, ctx):
        await ctx.send(f"Server has {len(ctx.guild.roles)} roles.")

    @commands.command(name="serverboosts")
    async def serverboosts(self, ctx):
        await ctx.send(f"Server has {ctx.guild.premium_subscription_count} boosts.")

    @commands.command(name="owner")
    async def owner(self, ctx):
        await ctx.send(f"Server owner: {ctx.guild.owner}")

    @commands.command(name="invite")
    async def invite(self, ctx):
        url = discord.utils.oauth_url(self.bot.user.id, permissions=discord.Permissions(permissions=8))
        await ctx.send(f"Invite me: {url}")

    @commands.command(name="pingrole")
    async def pingrole(self, ctx, role: discord.Role):
        await ctx.send(f"{role.mention}")

    @commands.command(name="emojis")
    async def emojis(self, ctx):
        emojis = ' '.join([str(e) for e in ctx.guild.emojis])
        await ctx.send(emojis or "No emojis.")

    @commands.command(name="boostlevel")
    async def boostlevel(self, ctx):
        await ctx.send(f"Boost level: {ctx.guild.premium_tier}")

    @commands.command(name="rules")
    async def rules(self, ctx):
        rules = ctx.guild.rules_channel
        if rules:
            await ctx.send(f"Rules channel: {rules.mention}")
        else:
            await ctx.send("No rules channel set.")

    @commands.command(name="verification")
    async def verification(self, ctx):
        await ctx.send(f"Verification level: {ctx.guild.verification_level}")

    @commands.command(name="memberslist")
    async def memberslist(self, ctx):
        members = ', '.join([m.name for m in ctx.guild.members[:50]])
        await ctx.send(f"Members: {members}... (first 50)")

async def setup(bot):
    import time
    bot.uptime = time.time()
    await bot.add_cog(General(bot))
