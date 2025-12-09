import discord
from discord.ext import commands
import random
import aiohttp

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ---------------- FUN PREFIX COMMANDS ----------------

    @commands.command(name="roll")
    async def roll(self, ctx):
        result = random.randint(1, 6)
        await ctx.send(f"🎲 You rolled a {result}!")

    @commands.command(name="flip")
    async def flip(self, ctx):
        result = random.choice(["Heads", "Tails"])
        await ctx.send(f"🪙 {result}!")

    @commands.command(name="8ball")
    async def eightball(self, ctx, *, question: str):
        responses = [
            "It is certain.", "Without a doubt.", "You may rely on it.",
            "Ask again later.", "Cannot predict now.", "Don't count on it.",
            "My sources say no.", "Very doubtful."
        ]
        answer = random.choice(responses)
        await ctx.send(f"🎱 Question: {question}\nAnswer: {answer}")

    @commands.command(name="joke")
    async def joke(self, ctx):
        jokes = [
            "Why did the chicken cross the road? To get to the other side!",
            "I told my computer I needed a break, and it said 'No problem – I'll go to sleep.'",
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "I would tell you a joke about UDP, but you might not get it."
        ]
        await ctx.send(random.choice(jokes))

    @commands.command(name="meme")
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://meme-api.com/gimme") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    await ctx.send(data['url'])
                else:
                    await ctx.send("Could not fetch a meme 😢")

    @commands.command(name="coinflip")
    async def coinflip(self, ctx):
        await self.flip(ctx)

    @commands.command(name="dice")
    async def dice(self, ctx):
        result = random.randint(1, 20)
        await ctx.send(f"🎲 You rolled a {result}!")

    @commands.command(name="compliment")
    async def compliment(self, ctx):
        compliments = [
            "You're amazing!", "You light up the room!", "You're a true star!"
        ]
        await ctx.send(random.choice(compliments))

    @commands.command(name="roast")
    async def roast(self, ctx):
        roasts = [
            "You're as bright as a black hole.", 
            "You're proof that evolution can go in reverse.", 
            "You bring everyone so much joy... when you leave the room."
        ]
        await ctx.send(random.choice(roasts))

    @commands.command(name="magic8ball")
    async def magic8ball(self, ctx, *, question: str):
        await self.eightball(ctx, question=question)

    @commands.command(name="randomnumber")
    async def randomnumber(self, ctx):
        num = random.randint(0, 1000)
        await ctx.send(f"🎲 Your random number is {num}")

    @commands.command(name="shrug")
    async def shrug(self, ctx):
        await ctx.send("¯\\_(ツ)_/¯")

    @commands.command(name="tableflip")
    async def tableflip(self, ctx):
        await ctx.send("(╯°□°）╯︵ ┻━┻")

    @commands.command(name="unflip")
    async def unflip(self, ctx):
        await ctx.send("┬─┬ ノ( ゜-゜ノ)")

    @commands.command(name="hug")
    async def hug(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send(f"🤗 {ctx.author.mention} hugs {member.mention}!")

    @commands.command(name="slap")
    async def slap(self, ctx, member: discord.Member):
        await ctx.send(f"👋 {ctx.author.mention} slaps {member.mention}!")

    @commands.command(name="highfive")
    async def highfive(self, ctx, member: discord.Member):
        await ctx.send(f"✋ {ctx.author.mention} high-fives {member.mention}!")

    @commands.command(name="pat")
    async def pat(self, ctx, member: discord.Member):
        await ctx.send(f"👋 {ctx.author.mention} pats {member.mention}!")

    @commands.command(name="dance")
    async def dance(self, ctx):
        await ctx.send(f"💃 {ctx.author.mention} is dancing!")

    @commands.command(name="laugh")
    async def laugh(self, ctx):
        await ctx.send(f"😂 {ctx.author.mention} is laughing!")

async def setup(bot):
    await bot.add_cog(Fun(bot))
