import discord
from discord.ext import commands
from discord import app_commands
import json
import os

SETTINGS_FILE = "logs_settings.json"

# ------------------ JSON HELPERS ------------------
def load_data():
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w") as f:
            json.dump({}, f, indent=4)
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ------------------ LOG TYPES ------------------
LOG_TYPES = [
    "main", "joins", "leaves", "edits", "deletes", "roles",
    "channels", "voice", "bans", "unbans", "boosts",
    "nicks", "timeouts", "role_add", "role_remove"
]

# ------------------ MAIN COG ------------------
class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ------------------ HELPERS ------------------
    def get_guild(self, guild_id: int):
        data = load_data()
        return data.get(str(guild_id), {})

    def update_guild(self, guild_id: int, new_data: dict):
        data = load_data()
        data[str(guild_id)] = new_data
        save_data(data)

    async def send_log(self, guild, log_type: str, embed: discord.Embed):
        data = self.get_guild(guild.id)
        if log_type not in data:
            return
        channel = guild.get_channel(data[log_type])
        if channel:
            await channel.send(embed=embed)

    # ------------------ PREFIX COMMAND ------------------
    @commands.group(name="logs", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def logs(self, ctx, log_type: str = None, channel: discord.TextChannel = None):
        if not log_type or not channel:
            await ctx.send("Usage: `!logs <log_type> <#channel>`")
            return
        log_type = log_type.lower()
        if log_type not in LOG_TYPES:
            await ctx.send(f"❌ Invalid log type. Valid types: {', '.join(LOG_TYPES)}")
            return

        data = self.get_guild(ctx.guild.id)
        data[log_type] = channel.id
        self.update_guild(ctx.guild.id, data)
        await ctx.send(f"✅ `{log_type}` logs set to {channel.mention}")

    @logs.command(name="disable")
    @commands.has_permissions(administrator=True)
    async def logs_disable(self, ctx):
        self.update_guild(ctx.guild.id, {})
        await ctx.send("❌ All logging disabled.")

    @logs.command(name="all")
    @commands.has_permissions(administrator=True)
    async def logs_all(self, ctx, channel: discord.TextChannel):
        data = {key: channel.id for key in LOG_TYPES}
        self.update_guild(ctx.guild.id, data)
        await ctx.send(f"📦 All logs set to {channel.mention}.")

    @logs.command(name="status")
    async def logs_status(self, ctx):
        data = self.get_guild(ctx.guild.id)
        embed = discord.Embed(title="📘 Log Settings", color=discord.Color.blue())
        for k, v in data.items():
            embed.add_field(name=k, value=f"<#{v}>")
        if not data:
            embed.description = "No logs configured."
        await ctx.send(embed=embed)

    # ------------------ SLASH COMMANDS ------------------
    @commands.command(name="logs-all")
    async def slash_logs_all(self, interaction: discord.Interaction, channel: discord.TextChannel):
        data = {key: channel.id for key in LOG_TYPES}
        self.update_guild(interaction.guild.id, data)
        await interaction.response.send_message(f"📦 All logs set to {channel.mention}")

    @commands.command(name="logs-status")
    async def slash_logs_status(self, interaction: discord.Interaction):
        data = self.get_guild(interaction.guild.id)
        embed = discord.Embed(title="📘 Log Settings", color=discord.Color.blue())
        for k, v in data.items():
            embed.add_field(name=k, value=f"<#{v}>")
        if not data:
            embed.description = "No logs configured."
        await interaction.response.send_message(embed=embed)

    # ------------------ EVENTS ------------------
    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(title="👋 Member Joined", description=f"{member.mention}", color=0x00FF00)
        await self.send_log(member.guild, "joins", embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(title="🚪 Member Left", description=f"{member.mention}", color=0xFF0000)
        await self.send_log(member.guild, "leaves", embed)

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        if msg.author.bot:
            return
        embed = discord.Embed(title="🗑 Message Deleted", color=0xDD0000)
        embed.add_field(name="Author", value=msg.author.mention)
        embed.add_field(name="Channel", value=msg.channel.mention)
        embed.add_field(name="Content", value=msg.content or "None")
        await self.send_log(msg.guild, "deletes", embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content:
            return
        embed = discord.Embed(title="✏ Message Edited", color=0xFFFF00)
        embed.add_field(name="Author", value=before.author.mention)
        embed.add_field(name="Before", value=before.content or "None", inline=False)
        embed.add_field(name="After", value=after.content or "None", inline=False)
        await self.send_log(before.guild, "edits", embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        # Nickname change
        if before.nick != after.nick:
            embed = discord.Embed(title="🏷 Nickname Changed", color=0x00CCFF)
            embed.add_field(name="Before", value=before.nick or "None")
            embed.add_field(name="After", value=after.nick or "None")
            await self.send_log(before.guild, "nicks", embed)

        # Role changes
        added = [r for r in after.roles if r not in before.roles]
        removed = [r for r in before.roles if r not in after.roles]
        for role in added:
            embed = discord.Embed(title="➕ Role Added", description=f"{after.mention}", color=0x00FFAA)
            embed.add_field(name="Role", value=role.name)
            await self.send_log(before.guild, "role_add", embed)
        for role in removed:
            embed = discord.Embed(title="➖ Role Removed", description=f"{after.mention}", color=0xFF5555)
            embed.add_field(name="Role", value=role.name)
            await self.send_log(before.guild, "role_remove", embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        embed = discord.Embed(title="📂 Channel Created", description=channel.name)
        await self.send_log(channel.guild, "channels", embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        embed = discord.Embed(title="🗑 Channel Deleted", description=channel.name)
        await self.send_log(channel.guild, "channels", embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        embed = discord.Embed(color=0x00AAFF)
        if before.channel is None and after.channel is not None:
            embed.title = "🎙 Voice Join"
            embed.description = f"{member.mention} joined {after.channel.name}"
        elif before.channel is not None and after.channel is None:
            embed.title = "📴 Voice Leave"
            embed.description = f"{member.mention} left {before.channel.name}"
        elif before.channel != after.channel:
            embed.title = "🔁 Voice Moved"
            embed.description = f"{member.mention} moved from {before.channel.name} to {after.channel.name}"
        else:
            return
        await self.send_log(member.guild, "voice", embed)

async def setup(bot):
    await bot.add_cog(Logs(bot))
