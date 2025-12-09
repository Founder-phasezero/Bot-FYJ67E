import discord
import json
from discord.ext import commands

# JSON file for reaction roles
FILE = "reaction_roles.json"

# -------------------------------------------------------
# JSON LOAD / SAVE
# -------------------------------------------------------
def load_data():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

REACTION_DATA = load_data()

# -------------------------------------------------------
# DROPDOWN MENU SYSTEM
# -------------------------------------------------------
class RoleMenu(discord.ui.Select):
    def __init__(self, role_list):
        options = [
            discord.SelectOption(label=role.name, value=str(role.id))
            for role in role_list
        ]
        super().__init__(placeholder="Choose your role…",
                         min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        role = interaction.guild.get_role(int(self.values[0]))
        await interaction.user.add_roles(role)
        await interaction.response.send_message(
            f"🎉 You received **{role.name}**!",
            ephemeral=True
        )

class RoleMenuView(discord.ui.View):
    def __init__(self, role_list):
        super().__init__(timeout=None)
        self.add_item(RoleMenu(role_list))

# -------------------------------------------------------
# MAIN COG
# -------------------------------------------------------
class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -------------------------------------------------------
    # HELPER — AUTO CREATE ROLE
    # -------------------------------------------------------
    async def create_or_get_role(self, guild, role_name, color):
        role = discord.utils.get(guild.roles, name=role_name)
        if role is None:
            role = await guild.create_role(name=role_name, color=color)
        return role

    # -------------------------------------------------------
    # PREFIX COMMANDS
    # -------------------------------------------------------

    @commands.command(name="rr_create")
    async def rr_create(self, ctx, title: str, *, description: str):
        embed = discord.Embed(title=title, description=description,
                              color=discord.Color.blurple())
        msg = await ctx.send(embed=embed)

        REACTION_DATA[str(msg.id)] = {}
        save_data(REACTION_DATA)

        await ctx.send(f"✅ Message created!\nID: `{msg.id}`")

    @commands.command(name="rr_add")
    async def rr_add(self, ctx, message_id: str, emoji: str, role: discord.Role):
        try:
            msg = await ctx.channel.fetch_message(int(message_id))
        except:
            return await ctx.send("❌ Invalid message ID.")

        await msg.add_reaction(emoji)

        if message_id not in REACTION_DATA:
            REACTION_DATA[message_id] = {}

        REACTION_DATA[message_id][emoji] = role.id
        save_data(REACTION_DATA)

        await ctx.send(f"✅ Added {emoji} → {role.mention}")

    @commands.command(name="rr_dropdown")
    async def rr_dropdown(self, ctx, role1: discord.Role, role2: discord.Role, role3: discord.Role):
        roles = [role1, role2, role3]

        embed = discord.Embed(
            title="🎭 Select Your Role",
            description="Choose a role using the dropdown below.",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed, view=RoleMenuView(roles))
        await ctx.send("✅ Dropdown panel created!")

    # -------------------------------------------------------
    # PANEL 1 — AUTO CREATE ROLES
    # -------------------------------------------------------
    @commands.command(name="rr_panel1")
    async def rr_panel1(self, ctx):
        guild = ctx.guild

        panel_roles = {
            "Fire Starter": discord.Color.red(),
            "Gamer Starter": discord.Color.green(),
            "Artist Starter": discord.Color.blue()
        }

        emojis = ["🔥", "🎮", "🎨"]

        embed = discord.Embed(
            title="🔥 Panel 1 — Starter Roles",
            description="React to get a starter role.",
            color=discord.Color.blue()
        )

        msg = await ctx.send(embed=embed)

        REACTION_DATA[str(msg.id)] = {}

        for (name, color), emoji in zip(panel_roles.items(), emojis):
            role = await self.create_or_get_role(guild, name, color)
            await msg.add_reaction(emoji)
            REACTION_DATA[str(msg.id)][emoji] = role.id

        save_data(REACTION_DATA)
        await ctx.send("Panel 1 created with auto-roles!")

    # -------------------------------------------------------
    # PANEL 2 — AUTO CREATE ROLES
    # -------------------------------------------------------
    @commands.command(name="rr_panel2")
    async def rr_panel2(self, ctx):
        guild = ctx.guild

        panel_roles = {
            "Book Lover": discord.Color.purple(),
            "Music Lover": discord.Color.orange(),
            "Tech Lover": discord.Color.teal()
        }

        emojis = ["📚", "🎵", "💻"]

        embed = discord.Embed(
            title="⭐ Panel 2 — Interest Roles",
            description="React to choose interests.",
            color=discord.Color.gold()
        )

        msg = await ctx.send(embed=embed)

        REACTION_DATA[str(msg.id)] = {}

        for (name, color), emoji in zip(panel_roles.items(), emojis):
            role = await self.create_or_get_role(guild, name, color)
            await msg.add_reaction(emoji)
            REACTION_DATA[str(msg.id)][emoji] = role.id

        save_data(REACTION_DATA)
        await ctx.send("Panel 2 created with auto-roles!")

    # -------------------------------------------------------
    # PANEL 3 — AUTO CREATE ROLES
    # -------------------------------------------------------
    @commands.command(name="rr_panel3")
    async def rr_panel3(self, ctx):
        guild = ctx.guild

        panel_roles = {
            "Diamond Member": discord.Color.blue(),
            "Lightning Member": discord.Color.yellow(),
            "Fire Premium": discord.Color.red()
        }

        emojis = ["💠", "⚡", "🔥"]

        embed = discord.Embed(
            title="💎 Panel 3 — Special Roles",
            description="React for premium/special roles.",
            color=discord.Color.purple()
        )

        msg = await ctx.send(embed=embed)

        REACTION_DATA[str(msg.id)] = {}

        for (name, color), emoji in zip(panel_roles.items(), emojis):
            role = await self.create_or_get_role(guild, name, color)
            await msg.add_reaction(emoji)
            REACTION_DATA[str(msg.id)][emoji] = role.id

        save_data(REACTION_DATA)
        await ctx.send("Panel 3 created with auto-roles!")

    # -------------------------------------------------------
    # CUSTOM UNLIMITED PANEL
    # -------------------------------------------------------
    @commands.command(name="rr_panel_custom")
    async def rr_panel_custom(self, ctx, title: str, description: str, *emoji_role_pairs):
        """
        Usage example:
        !rr_panel_custom "Game Roles" "Pick your platform" 🎮 @Gamer 🎧 1234567890123 💻 @PC
        """

        if len(emoji_role_pairs) % 2 != 0:
            return await ctx.send("❌ Please provide pairs: emoji + roleMention/roleID")

        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.random()
        )

        msg = await ctx.send(embed=embed)
        REACTION_DATA[str(msg.id)] = {}

        role_mentions = ctx.message.role_mentions

        mention_index = 0

        for i in range(0, len(emoji_role_pairs), 2):
            emoji = emoji_role_pairs[i]
            role_raw = emoji_role_pairs[i + 1]

            # Support role mention
            if role_raw.startswith("<@&"):
                role = role_mentions[mention_index]
                mention_index += 1
            else:
                role = ctx.guild.get_role(int(role_raw)) if role_raw.isdigit() else None

            if not role:
                await ctx.send(f"⚠ Could not find role `{role_raw}` — skipped.")
                continue

            try:
                await msg.add_reaction(emoji)
            except:
                await ctx.send(f"⚠ Invalid emoji `{emoji}` — skipped.")
                continue

            REACTION_DATA[str(msg.id)][emoji] = role.id

        save_data(REACTION_DATA)
        await ctx.send("✅ Custom reaction panel created!")

    # -------------------------------------------------------
    # REACTION LISTENERS
    # -------------------------------------------------------
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        msg_id = str(payload.message_id)
        if msg_id not in REACTION_DATA:
            return

        emoji = str(payload.emoji)
        if emoji not in REACTION_DATA[msg_id]:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member is None or member.bot:
            return

        role = guild.get_role(REACTION_DATA[msg_id][emoji])
        if role:
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        msg_id = str(payload.message_id)
        if msg_id not in REACTION_DATA:
            return

        emoji = str(payload.emoji)
        if emoji not in REACTION_DATA[msg_id]:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member is None or member.bot:
            return

        role = guild.get_role(REACTION_DATA[msg_id][emoji])
        if role:
            await member.remove_roles(role)

async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
