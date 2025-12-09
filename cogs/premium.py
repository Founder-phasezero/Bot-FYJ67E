import discord
from discord.ext import commands
import json
import os

PREMIUM_FILE = "premium_users.json"

# Ensure the file exists
if not os.path.exists(PREMIUM_FILE):
    with open(PREMIUM_FILE, "w") as f:
        json.dump([], f)

class Premium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load_premium_users()

    def load_premium_users(self):
        with open(PREMIUM_FILE, "r") as f:
            self.premium_users = json.load(f)

    def save_premium_users(self):
        with open(PREMIUM_FILE, "w") as f:
            json.dump(self.premium_users, f, indent=4)

    def is_premium(self, user_id):
        return user_id in self.premium_users

    # ---------------- PREMIUM PREFIX COMMANDS ----------------

    @commands.command(name="premiuminfo")
    async def premiuminfo(self, ctx):
        if self.is_premium(ctx.author.id):
            await ctx.send("🌟 You are a premium user!")
        else:
            await ctx.send("❌ You are not a premium user.")

    @commands.command(name="addpremium")
    @commands.has_permissions(administrator=True)
    async def addpremium(self, ctx, member: discord.Member):
        if member.id not in self.premium_users:
            self.premium_users.append(member.id)
            self.save_premium_users()
            await ctx.send(f"✅ {member.mention} added as premium.")
        else:
            await ctx.send(f"⚠️ {member.mention} is already a premium user.")

    @commands.command(name="removepremium")
    @commands.has_permissions(administrator=True)
    async def removepremium(self, ctx, member: discord.Member):
        if member.id in self.premium_users:
            self.premium_users.remove(member.id)
            self.save_premium_users()
            await ctx.send(f"✅ {member.mention} removed from premium.")
        else:
            await ctx.send(f"⚠️ {member.mention} is not a premium user.")

    @commands.command(name="boost")
    async def boost(self, ctx):
        if self.is_premium(ctx.author.id):
            await ctx.send("🚀 Boost activated! You used a premium-only command.")
        else:
            await ctx.send("❌ This command is for premium users only.")

async def setup(bot):
    await bot.add_cog(Premium(bot))
