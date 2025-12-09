import discord
from discord.ext import commands
import json
import os
import asyncio
import random
import string

FILE = "verified_users.json"
TIMEOUT = 300  # 5 minutes to complete verification

def load_data():
    if not os.path.exists(FILE):
        with open(FILE, "w") as f:
            json.dump({}, f)
    with open(FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.verified_users = load_data()

    # -------------------------- ,verify command --------------------------
    @commands.command(name="verify")
    async def verify(self, ctx):
        member = ctx.author
        guild = ctx.guild

        if str(member.id) in self.verified_users:
            await ctx.send("✅ You are already verified.")
            return

        captcha = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        embed = discord.Embed(
            title="🛡️ Verification",
            description=f"Please type the following CAPTCHA within {TIMEOUT//60} minutes:\n```\n{captcha}\n```",
            color=discord.Color.blue()
        )
        try:
            await member.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("❌ I couldn't DM you! Please enable DMs from server members.")
            return

        await ctx.send("✉️ Check your DMs to complete verification.")

        def check(m):
            return m.author == member and m.content.strip() == captcha

        try:
            await self.bot.wait_for("message", check=check, timeout=TIMEOUT)
        except asyncio.TimeoutError:
            await member.send("⏱️ Verification timed out! Please try ,verify again.")
            return

        role = discord.utils.get(guild.roles, name="Verified")
        if not role:
            role = await guild.create_role(name="Verified", color=discord.Color.green())
        await member.add_roles(role)

        self.verified_users[str(member.id)] = True
        save_data(self.verified_users)

        await member.send(f"🎉 Congratulations {member.name}! You are now verified in **{guild.name}**. Welcome!")

    # -------------------------- ,checkverify command --------------------------
    @commands.command(name="checkverify")
    async def check_verify(self, ctx, member: discord.Member):
        if str(member.id) in self.verified_users:
            await ctx.send(f"✅ {member.mention} is verified.")
        else:
            await ctx.send(f"❌ {member.mention} is NOT verified.")

    # -------------------------- ,unverify command (admin) --------------------------
    @commands.command(name="unverify")
    @commands.has_permissions(manage_roles=True)
    async def unverify(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Verified")
        if role in member.roles:
            await member.remove_roles(role)
        self.verified_users.pop(str(member.id), None)
        save_data(self.verified_users)
        await ctx.send(f"⚠️ {member.mention} has been unverified.")

    # -------------------------- ,verifypanel command (admin) --------------------------
    @commands.command(name="verifypanel")
    @commands.has_permissions(administrator=True)
    async def verifypanel(self, ctx, channel: discord.TextChannel = None):
        """Send a verification panel in the specified channel"""
        channel = channel or ctx.channel
        embed = discord.Embed(
            title="✅ Verification Panel",
            description="React with ✅ to verify yourself and get access to the server!",
            color=discord.Color.green()
        )
        message = await channel.send(embed=embed)
        await message.add_reaction("✅")

        def check(reaction, user):
            return str(reaction.emoji) == "✅" and not user.bot and reaction.message.id == message.id

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=None, check=check)
                role = discord.utils.get(ctx.guild.roles, name="Verified")
                if not role:
                    role = await ctx.guild.create_role(name="Verified", color=discord.Color.green())
                if role not in user.roles:
                    await user.add_roles(role)
                    self.verified_users[str(user.id)] = True
                    save_data(self.verified_users)
                    await user.send(f"🎉 You are now verified in **{ctx.guild.name}**!")
            except Exception as e:
                print(f"Verification panel error: {e}")

async def setup(bot):
    await bot.add_cog(Verify(bot))
