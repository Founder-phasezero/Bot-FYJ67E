import discord
from discord.ext import commands
import random
import datetime
import asyncio

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ---------------- UTILITY COMMANDS ----------------

    @commands.command(name="userinfo")
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"User Info: {member}", color=discord.Color.blue())
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime('%Y-%m-%d'))
        embed.add_field(name="Created Account", value=member.created_at.strftime('%Y-%m-%d'))
        embed.set_thumbnail(url=member.avatar.url if member.avatar else discord.Embed.Empty)
        await ctx.send(embed=embed)

    @commands.command(name="serverinfo")
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"Server Info: {guild.name}", color=discord.Color.green())
        embed.add_field(name="ID", value=guild.id)
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name="Owner", value=guild.owner)
        embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)
        await ctx.send(embed=embed)

    @commands.command(name="avatar")
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send(member.avatar.url if member.avatar else "❌ No avatar found.")

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send(f"🏓 Pong! {round(self.bot.latency*1000)}ms")

    @commands.command(name="randomnumber")
    async def randomnumber(self, ctx, min: int, max: int):
        await ctx.send(f"🎲 Random number: {random.randint(min, max)}")

    @commands.command(name="time")
    async def time(self, ctx):
        now = datetime.datetime.now()
        await ctx.send(f"⏰ Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    @commands.command(name="flipcoin")
    async def flipcoin(self, ctx):
        await ctx.send(f"🪙 {random.choice(['Heads', 'Tails'])}")

    @commands.command(name="roll")
    async def roll(self, ctx, sides: int = 6):
        await ctx.send(f"🎲 Rolled: {random.randint(1, sides)}")

    @commands.command(name="quote")
    async def quote(self, ctx):
        quotes = ["Stay positive!", "Never give up!", "You can do it!"]
        await ctx.send(f"💡 {random.choice(quotes)}")

    @commands.command(name="weather")
    async def weather(self, ctx, *, location: str):
        await ctx.send(f"🌤️ Weather in {location}: 25°C, Sunny (demo)")

    @commands.command(name="calculator")
    async def calculator(self, ctx, a: int, b: int):
        await ctx.send(f"🧮 {a} + {b} = {a+b}")

    @commands.command(name="define")
    async def define(self, ctx, *, word: str):
        await ctx.send(f"📖 {word}: A demonstration definition.")

    @commands.command(name="servericon")
    async def servericon(self, ctx):
        if ctx.guild.icon:
            await ctx.send(ctx.guild.icon.url)
        else:
            await ctx.send("❌ Server has no icon.")

    @commands.command(name="uptime")
    async def uptime(self, ctx):
        await ctx.send("⏱️ Bot has been online for 2 hours (demo)")

    @commands.command(name="remindme")
    async def remindme(self, ctx, seconds: int, *, message: str):
        await ctx.send(f"⏳ Reminder set for {seconds} seconds")
        await asyncio.sleep(seconds)
        await ctx.send(f"🔔 Reminder: {message}")

    @commands.command(name="say")
    async def say(self, ctx, *, message: str):
        await ctx.send(message)

    @commands.command(name="choose")
    async def choose(self, ctx, *options: str):
        if options:
            await ctx.send(f"🎲 Chosen: {random.choice(options)}")
        else:
            await ctx.send("❌ No options provided.")

    @commands.command(name="echo")
    async def echo(self, ctx, *, text: str):
        await ctx.send(text)

    @commands.command(name="joke")
    async def joke(self, ctx):
        jokes = [
            "Why did the chicken cross the road? To get to the other side!",
            "I told my computer I needed a break, and it said no problem — it needed one too!"
        ]
        await ctx.send(random.choice(jokes))

    @commands.command(name="pingtest")
    async def pingtest(self, ctx):
        await ctx.send(f"🏓 Pong! {round(self.bot.latency*1000)}ms")


async def setup(bot):
    await bot.add_cog(Utility(bot))
