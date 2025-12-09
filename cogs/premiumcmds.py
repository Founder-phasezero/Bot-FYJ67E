import discord
from discord.ext import commands
import json
import os
import random

PREMIUM_FILE = "premium_users.json"

# Ensure the premium JSON exists
if not os.path.exists(PREMIUM_FILE):
    with open(PREMIUM_FILE, "w") as f:
        json.dump([], f)

class PremiumCommands(commands.Cog):
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

    # ---------------- PREMIUM COMMANDS ----------------

    @commands.command(name="dailyreward")
    async def dailyreward(self, ctx):
        if self.is_premium(ctx.author.id):
            await ctx.send("🎁 You claimed your daily premium reward!")
        else:
            await ctx.send("❌ Only premium users can claim this reward.")

    @commands.command(name="specialrole")
    async def specialrole(self, ctx):
        if self.is_premium(ctx.author.id):
            role = discord.utils.get(ctx.guild.roles, name="Premium")
            if not role:
                role = await ctx.guild.create_role(name="Premium")
            await ctx.author.add_roles(role)
            await ctx.send(f"🌟 {ctx.author.mention} received the Premium role!")
        else:
            await ctx.send("❌ Only premium users can get the premium role.")

    @commands.command(name="exclusiveemoji")
    async def exclusiveemoji(self, ctx):
        if self.is_premium(ctx.author.id):
            await ctx.send("😎 You used a premium emoji!")
        else:
            await ctx.send("❌ Only premium users can use this emoji.")

    @commands.command(name="vipchat")
    async def vipchat(self, ctx):
        if self.is_premium(ctx.author.id):
            # Get or create Premium role
            premium_role = discord.utils.get(ctx.guild.roles, name="Premium")
            if not premium_role:
                premium_role = await ctx.guild.create_role(name="Premium")

            # Check if VIP channel exists
            existing_channel = discord.utils.get(ctx.guild.channels, name="vip-chat")
            if existing_channel:
                await ctx.send(f"💬 VIP chat already exists: {existing_channel.mention}")
                return

            # Create VIP channel
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                premium_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            channel = await ctx.guild.create_text_channel("vip-chat", overwrites=overwrites)
            await ctx.send(f"💬 VIP chat created: {channel.mention}")
        else:
            await ctx.send("❌ Only premium users can access VIP chat.")

    @commands.command(name="premiumgift")
    async def premiumgift(self, ctx):
        if self.is_premium(ctx.author.id):
            await ctx.send(f"🎁 {ctx.author.mention} sent a premium gift!")
        else:
            await ctx.send("❌ Only premium users can send gifts.")

    @commands.command(name="premiumquote")
    async def premiumquote(self, ctx):
        if self.is_premium(ctx.author.id):
            quotes = ["Stay legendary!", "Only the best deserve this.", "Premium life! 😎"]
            await ctx.send(random.choice(quotes))
        else:
            await ctx.send("❌ Only premium users can get premium quotes.")

    @commands.command(name="flashboost")
    async def flashboost(self, ctx):
        if self.is_premium(ctx.author.id):
            await ctx.send("⚡ Flash boost activated!")
        else:
            await ctx.send("❌ Only premium users can use this command.")

    @commands.command(name="premiumbadge")
    async def premiumbadge(self, ctx):
        if self.is_premium(ctx.author.id):
            await ctx.send("🏅 You have a premium badge!")
        else:
            await ctx.send("❌ Only premium users have badges.")

    @commands.command(name="exclusivechat")
    async def exclusivechat(self, ctx, *, message: str):
        if self.is_premium(ctx.author.id):
            await ctx.send(f"🗨️ [VIP] {ctx.author.mention}: {message}")
        else:
            await ctx.send("❌ Only premium users can chat here.")

    @commands.command(name="premiumemote")
    async def premiumemote(self, ctx):
        if self.is_premium(ctx.author.id):
            await ctx.send("🎭 Premium emote activated!")
        else:
            await ctx.send("❌ Only premium users can send premium emotes.")

    @commands.command(name="vipstatus")
    async def vipstatus(self, ctx):
        if self.is_premium(ctx.author.id):
            await ctx.send("🌟 VIP Status: Active")
        else:
            await ctx.send("❌ You are not VIP.")

    @commands.command(name="premiumping")
    async def premiumping(self, ctx):
        if self.is_premium(ctx.author.id):
            await ctx.send("🏓 Pinging premium servers...")
        else:
            await ctx.send("❌ Only premium users can ping.")

    @commands.command(name="premiumchallenge")
    async def premiumchallenge(self, ctx):
        if self.is_premium(ctx.author.id):
            await ctx.send("🔥 Premium challenge started!")
        else:
            await ctx.send("❌ Only premium users can start challenges.")

    @commands.command(name="exclusivecontent")
    async def exclusivecontent(self, ctx):
        if self.is_premium(ctx.author.id):
            await ctx.send("📦 Here is your exclusive premium content!")
        else:
            await ctx.send("❌ Only premium users can access exclusive content.")

    @commands.command(name="premiumfun")
    async def premiumfun(self, ctx):
        if self.is_premium(ctx.author.id):
            await ctx.send("🎉 Premium fun activated!")
        else:
            await ctx.send("❌ Only premium users can do this.")

    @commands.command(name="vipgift")
    async def vipgift(self, ctx):
        if self.is_premium(ctx.author.id):
            await ctx.send("🎁 You received a VIP gift!")
        else:
            await ctx.send("❌ Only premium users can receive VIP gifts.")

    @commands.command(name="premiumevent")
    async def premiumevent(self, ctx):
        if self.is_premium(ctx.author.id):
            await ctx.send("🏆 Joined premium event!")
        else:
            await ctx.send("❌ Only premium users can join events.")

    @commands.command(name="premiumvip")
    async def premiumvip(self, ctx):
        if self.is_premium(ctx.author.id):
            await ctx.send("🚀 VIP features activated!")
        else:
            await ctx.send("❌ Only premium users can activate VIP features.")

    @commands.command(name="premiumpoints")
    async def premiumpoints(self, ctx):
        if self.is_premium(ctx.author.id):
            await ctx.send("💎 You have 100 premium points!")
        else:
            await ctx.send("❌ Only premium users have points.")

async def setup(bot):
    await bot.add_cog(PremiumCommands(bot))
