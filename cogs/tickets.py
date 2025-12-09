import discord
from discord.ext import commands
from discord.ui import View, Button
import json
import os
import asyncio

DATA_FILE = "ticket_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"counter": 0, "staff_role": None}, f, indent=4)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- TRANSLATIONS ---------------- #

LANG = {
    "ticket_claimed": {"en": "🛠 Ticket claimed by {}"},
    "closing_ticket": {"en": "🗑 Closing ticket..."},
}

def t(key):
    return LANG[key]["en"]

# ---------------- CLAIM BUTTON ---------------- #

class ClaimTicketButton(Button):
    def __init__(self):
        super().__init__(label="Claim Ticket", style=discord.ButtonStyle.blurple)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            t("ticket_claimed").format(interaction.user.mention)
        )
        await interaction.channel.send(
            f"🛠 Ticket is now claimed by **{interaction.user}**"
        )

# ---------------- CLOSE BUTTON ---------------- #

class CloseTicketButton(Button):
    def __init__(self):
        super().__init__(label="Close Ticket", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(t("closing_ticket"), ephemeral=True)
        await interaction.channel.delete()

# ---------------- TICKET BUTTON ---------------- #

class TicketButton(Button):
    def __init__(self, label, category_name):
        super().__init__(label=label, style=discord.ButtonStyle.green)
        self.reason = label
        self.category_name = category_name

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        guild = interaction.guild
        data = load_data()

        # Prevent duplicate tickets
        for ch in guild.text_channels:
            if ch.topic and f"user:{user.id}" in ch.topic:
                return await interaction.response.send_message(
                    f"❌ You already have a ticket open: {ch.mention}",
                    ephemeral=True
                )

        # Find or create category
        category = discord.utils.get(guild.categories, name=self.category_name)
        if not category:
            category = await guild.create_category(self.category_name)

        # Auto ticket number
        data["counter"] += 1
        number = str(data["counter"]).zfill(3)
        save_data(data)

        safe_user = user.name.replace(" ", "-").lower()
        safe_reason = self.reason.replace(" ", "-").lower()

        channel_name = f"ticket-{number}-{safe_reason}-{safe_user}"

        # Create ticket
        channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            topic=f"user:{user.id} | reason:{self.reason}"
        )

        await channel.set_permissions(user, read_messages=True, send_messages=True)
        await channel.set_permissions(guild.default_role, read_messages=False)

        # Staff role ping
        staff_role_id = data.get("staff_role")
        if staff_role_id:
            role = guild.get_role(staff_role_id)
            if role:
                await channel.send(role.mention)

        # Buttons inside ticket
        view = View()
        view.add_item(ClaimTicketButton())
        view.add_item(CloseTicketButton())

        await channel.send(f"{user.mention}\n🎟 **Reason:** {self.reason}", view=view)

        await interaction.response.send_message(
            f"🎫 Ticket created: {channel.mention}",
            ephemeral=True
        )

# ---------------- PANEL COMMAND ---------------- #

class TicketPanelCustom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ticketpanel")
    async def ticketpanel_custom(self, ctx, *, args):
        """
        Format:
        Title | Description | Button1:Category | Button2:Category | Button3:Category
        """

        parts = [x.strip() for x in args.split("|")]

        if len(parts) < 3:
            return await ctx.send(
                "❌ Format: `Title | Description | Button1:Category | Button2:Category...`"
            )

        title = parts[0]
        description = parts[1]
        button_pairs = parts[2:]

        embed = discord.Embed(title=title, description=description, color=discord.Color.blue())

        view = View()
        for pair in button_pairs:
            if ":" not in pair:
                return await ctx.send("❌ Each button must be `Button:Category`")

            label, category = pair.split(":", 1)
            view.add_item(TicketButton(label.strip(), category.strip()))

        await ctx.send(embed=embed, view=view)
        await ctx.send("✅ Custom ticket panel created!")

    # ---------------- TRANSCRIPT ---------------- #

    @commands.command(name="transcript")
    async def transcript(self, ctx):
        messages = []
        async for msg in ctx.channel.history(limit=None, oldest_first=True):
            messages.append(f"{msg.author}: {msg.content}")

        file_name = f"transcript-{ctx.channel.name}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(messages))

        await ctx.send("📄 Transcript generated:", file=discord.File(file_name))

    # ---------------- SET STAFF ROLE ---------------- #

    @commands.command(name="ticketstaff")
    @commands.has_permissions(administrator=True)
    async def set_staff(self, ctx, role: discord.Role):
        data = load_data()
        data["staff_role"] = role.id
        save_data(data)
        await ctx.send(f"✅ Staff role set to {role.mention}")

async def setup(bot):
    await bot.add_cog(TicketPanelCustom(bot))
