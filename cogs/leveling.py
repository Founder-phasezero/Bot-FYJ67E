import discord
from discord.ext import commands
import json
import os

FILE = "levels.json"
XP_PER_MESSAGE = 10
LEVEL_MULTIPLIER = 100  # XP needed = level * LEVEL_MULTIPLIER

def load_data():
    if not os.path.exists(FILE):
        with open(FILE, "w") as f:
            json.dump({}, f)
    with open(FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = load_data()

    # ------------------------------ XP Gain Listener ------------------------------
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        self.data = load_data()
        user_id = str(message.author.id)

        if user_id not in self.data:
            self.data[user_id] = {"xp": 0, "level": 1}

        self.data[user_id]["xp"] += XP_PER_MESSAGE
        xp = self.data[user_id]["xp"]
        level = self.data[user_id]["level"]

        if xp >= level * LEVEL_MULTIPLIER:
            self.data[user_id]["level"] += 1
            self.data[user_id]["xp"] = xp - (level * LEVEL_MULTIPLIER)
            await message.channel.send(
                f"🎉 {message.author.mention} has leveled up to **Level {self.data[user_id]['level']}!**"
            )

        save_data(self.data)

    # ------------------------------ Level command ------------------------------
    @commands.command(name="level")
    async def level_prefix(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        self.data = load_data()
        user_id = str(member.id)

        if user_id not in self.data:
            await ctx.send(f"❌ {member.display_name} has no XP yet.")
            return

        xp = self.data[user_id]["xp"]
        level = self.data[user_id]["level"]
        next_level_xp = level * LEVEL_MULTIPLIER

        embed = discord.Embed(title=f"{member.display_name}'s Level", color=discord.Color.green())
        embed.add_field(name="Level", value=level)
        embed.add_field(name="XP", value=f"{xp}/{next_level_xp}")

        await ctx.send(embed=embed)

    # ------------------------------ Leaderboard command ------------------------------
    @commands.command(name="leaderboard")
    async def leaderboard_prefix(self, ctx):
        self.data = load_data()
        leaderboard = sorted(self.data.items(), key=lambda x: (x[1]["level"], x[1]["xp"]), reverse=True)[:10]

        embed = discord.Embed(title="🏆 Level Leaderboard", color=discord.Color.gold())
        for i, (user_id, stats) in enumerate(leaderboard, 1):
            user = ctx.guild.get_member(int(user_id))
            name = user.display_name if user else f"User Left ({user_id})"
            embed.add_field(name=f"{i}. {name}", value=f"Level {stats['level']} — {stats['xp']} XP", inline=False)

        await ctx.send(embed=embed)

    # ------------------------------ Admin commands ------------------------------
    @commands.command(name="setlevel")
    @commands.has_permissions(administrator=True)
    async def set_level(self, ctx, member: discord.Member, level: int):
        """Set a member's level manually."""
        self.data = load_data()
        user_id = str(member.id)
        if user_id not in self.data:
            self.data[user_id] = {"xp": 0, "level": 1}
        self.data[user_id]["level"] = level
        self.data[user_id]["xp"] = 0
        save_data(self.data)
        await ctx.send(f"✅ Set **{member.display_name}**'s level to **{level}** and XP reset to 0.")

    @commands.command(name="dellevel")
    @commands.has_permissions(administrator=True)
    async def delete_level(self, ctx, member: discord.Member):
        """Reset a member's level and XP."""
        self.data = load_data()
        user_id = str(member.id)
        if user_id in self.data:
            del self.data[user_id]
            save_data(self.data)
            await ctx.send(f"🗑 Reset level and XP for **{member.display_name}**.")
        else:
            await ctx.send(f"❌ {member.display_name} has no XP/level data.")

    @commands.command(name="addlevel")
    @commands.has_permissions(administrator=True)
    async def add_level(self, ctx, member: discord.Member, amount: int):
        """Add levels to a member without changing XP."""
        self.data = load_data()
        user_id = str(member.id)
        if user_id not in self.data:
            self.data[user_id] = {"xp": 0, "level": 1}
        self.data[user_id]["level"] += amount
        save_data(self.data)
        await ctx.send(f"➕ Added **{amount}** level(s) to **{member.display_name}**. New level: {self.data[user_id]['level']}")

async def setup(bot):
    await bot.add_cog(Leveling(bot))
