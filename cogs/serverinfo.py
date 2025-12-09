import discord
from discord.ext import commands

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="serverinfo")
    async def serverinfo(self, ctx):
        guild = ctx.guild

        # Member stats
        total_members = guild.member_count
        online_members = sum(1 for m in guild.members if m.status != discord.Status.offline)
        bots = sum(1 for m in guild.members if m.bot)

        # Channel stats
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)

        # Roles and emojis
        roles = len(guild.roles)
        emojis = len(guild.emojis)

        # Boost info
        boosts = guild.premium_subscription_count
        tier = guild.premium_tier

        # Vanity URL
        vanity_url = getattr(guild, "vanity_url_code", None)
        vanity_url_text = f"https://discord.gg/{vanity_url}" if vanity_url else "None"

        # Top boosters
        boosters = [m for m in guild.members if m.premium_since]
        top_boosters = sorted(boosters, key=lambda m: m.premium_since)[:5]
        top_boosters_text = "\n".join([f"{b.mention} — Boosted since {b.premium_since.date()}" for b in top_boosters]) or "No boosters"

        # Create embed
        embed = discord.Embed(
            title=f"📊 Server Info: {guild.name}",
            color=discord.Color.blurple()
        )

        # Icon and banner
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        if guild.banner:
            embed.set_image(url=guild.banner.url)

        # Fields
        embed.add_field(name="Server ID", value=guild.id, inline=True)
        embed.add_field(name="Owner", value=guild.owner, inline=True)
        embed.add_field(name="Created On", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)

        embed.add_field(name="Members", value=f"Total: {total_members}\nOnline: {online_members}\nBots: {bots}", inline=False)
        embed.add_field(name="Channels", value=f"Text: {text_channels}\nVoice: {voice_channels}\nCategories: {categories}", inline=False)
        embed.add_field(name="Roles", value=roles, inline=True)
        embed.add_field(name="Emojis", value=emojis, inline=True)

        embed.add_field(name="Boost Info", value=f"Tier {tier} — {boosts} boosts", inline=False)
        embed.add_field(name="Top Boosters", value=top_boosters_text, inline=False)
        embed.add_field(name="Vanity URL", value=vanity_url_text, inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerInfo(bot))
