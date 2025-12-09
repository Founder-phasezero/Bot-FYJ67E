import discord
from discord.ext import commands
import json
import os

SETTINGS_FILE = "welcome_settings.json"

def load_data():
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w") as f:
            json.dump({}, f, indent=4)
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ---------- Helper ----------
    def get_guild(self, guild_id):
        data = load_data()
        return data.get(str(guild_id), {})

    def update_guild(self, guild_id, new_data):
        data = load_data()
        data[str(guild_id)] = new_data
        save_data(data)

    # ---------- EVENTS ----------
    @commands.Cog.listener()
    async def on_member_join(self, member):
        data = self.get_guild(member.guild.id)
        if not data.get("enabled", False):
            return

        channel_id = data.get("channel")
        if channel_id is None:
            return

        channel = member.guild.get_channel(channel_id)
        if channel is None:
            return

        message = data.get("welcome_message", "Welcome to the server!")
        await channel.send(message.replace("{user}", member.mention))

        # DM welcome
        if data.get("dm_enabled"):
            dm_text = data.get("dm_message", "Welcome!")
            try:
                await member.send(dm_text.replace("{user}", member.name))
            except:
                pass

        # Autorole
        role_id = data.get("autorole")
        if role_id:
            role = member.guild.get_role(role_id)
            if role:
                try:
                    await member.add_roles(role)
                except:
                    pass

    # ---------- PREFIX COMMANDS ----------
    @commands.command(name="welcome-enable")
    async def welcome_enable(self, ctx):
        data = self.get_guild(ctx.guild.id)
        data["enabled"] = True
        self.update_guild(ctx.guild.id, data)
        await ctx.send("✅ Welcome system **enabled**.")

    @commands.command(name="welcome-disable")
    async def welcome_disable(self, ctx):
        data = self.get_guild(ctx.guild.id)
        data["enabled"] = False
        self.update_guild(ctx.guild.id, data)
        await ctx.send("❌ Welcome system **disabled**.")

    @commands.command(name="welcome-set-channel")
    async def welcome_set_channel(self, ctx, channel: discord.TextChannel):
        data = self.get_guild(ctx.guild.id)
        data["channel"] = channel.id
        self.update_guild(ctx.guild.id, data)
        await ctx.send(f"📩 Welcome channel set to {channel.mention}")

    @commands.command(name="welcome-set-message")
    async def welcome_set_message(self, ctx, *, message: str):
        data = self.get_guild(ctx.guild.id)
        data["welcome_message"] = message
        self.update_guild(ctx.guild.id, data)
        await ctx.send("✏ Welcome message updated.")

    @commands.command(name="welcome-test")
    async def welcome_test(self, ctx):
        data = self.get_guild(ctx.guild.id)
        text = data.get("welcome_message", "Welcome!")
        await ctx.send(text.replace("{user}", ctx.author.mention))

    @commands.command(name="welcome-status")
    async def welcome_status(self, ctx):
        data = self.get_guild(ctx.guild.id)
        embed = discord.Embed(title="📥 Welcome System Status", color=discord.Color.blue())
        embed.add_field(name="Enabled", value=str(data.get("enabled", False)))
        embed.add_field(name="Channel", value=f"<#{data.get('channel')}>" if data.get("channel") else "None")
        embed.add_field(name="Message", value=data.get("welcome_message", "Not set"), inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="welcome-autorole")
    async def welcome_autorole(self, ctx, role: discord.Role):
        data = self.get_guild(ctx.guild.id)
        data["autorole"] = role.id
        self.update_guild(ctx.guild.id, data)
        await ctx.send(f"🔧 Autorole set to **{role.name}**.")

    @commands.command(name="welcome-autorole-off")
    async def welcome_autorole_off(self, ctx):
        data = self.get_guild(ctx.guild.id)
        data["autorole"] = None
        self.update_guild(ctx.guild.id, data)
        await ctx.send("❌ Autorole disabled.")

    @commands.command(name="welcome-dm-enable")
    async def welcome_dm_enable(self, ctx):
        data = self.get_guild(ctx.guild.id)
        data["dm_enabled"] = True
        self.update_guild(ctx.guild.id, data)
        await ctx.send("📨 DM welcome **enabled**.")

    @commands.command(name="welcome-dm-disable")
    async def welcome_dm_disable(self, ctx):
        data = self.get_guild(ctx.guild.id)
        data["dm_enabled"] = False
        self.update_guild(ctx.guild.id, data)
        await ctx.send("❌ DM welcome **disabled**.")

    @commands.command(name="welcome-set-dm-message")
    async def welcome_set_dm(self, ctx, *, message: str):
        data = self.get_guild(ctx.guild.id)
        data["dm_message"] = message
        self.update_guild(ctx.guild.id, data)
        await ctx.send("📨 DM message updated.")

    @commands.command(name="welcome-reset")
    async def welcome_reset(self, ctx):
        self.update_guild(ctx.guild.id, {})
        await ctx.send("♻ Welcome settings reset.")

    @commands.command(name="welcome-counter")
    async def welcome_counter(self, ctx, channel: discord.TextChannel):
        data = self.get_guild(ctx.guild.id)
        data["counter"] = channel.id
        self.update_guild(ctx.guild.id, data)
        await ctx.send("🔢 Member counter enabled.")

    @commands.command(name="welcome-counter-disable")
    async def welcome_counter_disable(self, ctx):
        data = self.get_guild(ctx.guild.id)
        data["counter"] = None
        self.update_guild(ctx.guild.id, data)
        await ctx.send("❌ Member counter disabled.")

    @commands.command(name="welcome-preview")
    async def welcome_preview(self, ctx):
        data = self.get_guild(ctx.guild.id)
        msg = data.get("welcome_message", "Welcome {user}!")
        embed = discord.Embed(title="👋 Welcome Preview", description=msg.replace("{user}", ctx.author.name))
        await ctx.send(embed=embed)

    @commands.command(name="welcome-logjoins")
    async def welcome_logjoins(self, ctx, channel: discord.TextChannel):
        data = self.get_guild(ctx.guild.id)
        data["join_log"] = channel.id
        self.update_guild(ctx.guild.id, data)
        await ctx.send("📘 Join logs enabled.")

    @commands.command(name="welcome-logleaves")
    async def welcome_logleaves(self, ctx, channel: discord.TextChannel):
        data = self.get_guild(ctx.guild.id)
        data["leave_log"] = channel.id
        self.update_guild(ctx.guild.id, data)
        await ctx.send("📕 Leave logs enabled.")

    @commands.command(name="welcome-info")
    async def welcome_info(self, ctx):
        await ctx.send(
            "Variables:\n"
            "`{user}` → Mention the new user\n"
            "`{username}` → Username\n"
            "`{server}` → Server name"
        )


async def setup(bot):
    await bot.add_cog(Welcome(bot))
