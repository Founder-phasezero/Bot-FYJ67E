import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ------------------------------
    # Bot is ready
    # ------------------------------
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ Bot is online: {self.bot.user} (ID: {self.bot.user.id})")

    # ------------------------------
    # Member join
    # ------------------------------
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = discord.utils.get(member.guild.text_channels, name="welcome")
        if channel:
            await channel.send(f"🎉 Welcome {member.mention} to **{member.guild.name}**!")

    # ------------------------------
    # Member leave
    # ------------------------------
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        channel = discord.utils.get(member.guild.text_channels, name="welcome")
        if channel:
            await channel.send(f"👋 {member.mention} has left **{member.guild.name}**.")

    # ------------------------------
    # Member update (nickname / roles)
    # ------------------------------
    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        changes = []
        if before.nick != after.nick:
            changes.append(f"Nickname: {before.nick} ➔ {after.nick}")
        if before.roles != after.roles:
            changes.append("Roles updated")
        if changes:
            log_channel = discord.utils.get(after.guild.text_channels, name="logs")
            if log_channel:
                await log_channel.send(f"✏️ {after.mention} updated:\n" + "\n".join(changes))

    # ------------------------------
    # Message edits
    # ------------------------------
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.content != after.content:
            log_channel = discord.utils.get(before.guild.text_channels, name="logs")
            if log_channel:
                await log_channel.send(
                    f"📝 Message edited by {before.author.mention}:\nBefore: {before.content}\nAfter: {after.content}"
                )

    # ------------------------------
    # Message deletes
    # ------------------------------
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot:
            return
        log_channel = discord.utils.get(message.guild.text_channels, name="logs")
        if log_channel:
            await log_channel.send(
                f"❌ Message deleted from {message.author.mention}:\n{message.content}"
            )

    # ------------------------------
    # Reaction add
    # ------------------------------
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        if user.bot:
            return
        log_channel = discord.utils.get(reaction.message.guild.text_channels, name="logs")
        if log_channel:
            await log_channel.send(
                f"➕ {user.mention} added reaction {reaction.emoji} to message ID {reaction.message.id}"
            )

    # ------------------------------
    # Reaction remove
    # ------------------------------
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User):
        if user.bot:
            return
        log_channel = discord.utils.get(reaction.message.guild.text_channels, name="logs")
        if log_channel:
            await log_channel.send(
                f"➖ {user.mention} removed reaction {reaction.emoji} from message ID {reaction.message.id}"
            )

async def setup(bot):
    await bot.add_cog(Events(bot))
