import discord
from discord.ext import commands
import json
import os

FILE = "autoresponses.json"

def load_data():
    if not os.path.exists(FILE):
        with open(FILE, "w") as f:
            json.dump({"enabled": True, "responses": {}}, f, indent=4)
    with open(FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


class AutoResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = load_data()

    # -----------------------------------------
    # AUTORESPONSE LISTENER
    # -----------------------------------------
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        self.data = load_data()
        if not self.data["enabled"]:
            return

        msg = message.content.lower()

        for keyword, reply in self.data["responses"].items():
            if keyword.lower() in msg:
                await message.channel.send(reply)
                return

    # -----------------------------------------
    # ADD AUTORESPONSE
    # -----------------------------------------
    @commands.command(name="auto-add")
    @commands.has_permissions(manage_guild=True)
    async def auto_add(self, ctx, keyword: str, *, reply: str):
        self.data = load_data()
        self.data["responses"][keyword] = reply
        save_data(self.data)
        await ctx.send(
            f"✅ Added autoresponse:\n**When someone says:** `{keyword}`\n**Bot replies:** `{reply}`"
        )

    # -----------------------------------------
    # REMOVE AUTORESPONSE
    # -----------------------------------------
    @commands.command(name="auto-remove")
    @commands.has_permissions(manage_guild=True)
    async def auto_remove(self, ctx, keyword: str):
        self.data = load_data()
        if keyword not in self.data["responses"]:
            await ctx.send("❌ That keyword does not exist.")
            return

        del self.data["responses"][keyword]
        save_data(self.data)
        await ctx.send(f"🗑️ Removed autoresponse for `{keyword}`.")

    # -----------------------------------------
    # LIST AUTORESPONDERS
    # -----------------------------------------
    @commands.command(name="auto-list")
    async def auto_list(self, ctx):
        self.data = load_data()
        if len(self.data["responses"]) == 0:
            await ctx.send("📭 No autoresponders set.")
            return

        embed = discord.Embed(
            title="🤖 Autoresponder List",
            color=discord.Color.blurple()
        )

        for keyword, reply in self.data["responses"].items():
            embed.add_field(name=keyword, value=reply, inline=False)

        await ctx.send(embed=embed)

    # -----------------------------------------
    # ENABLE / DISABLE AUTORESPONDER
    # -----------------------------------------
    @commands.command(name="auto-toggle")
    @commands.has_permissions(manage_guild=True)
    async def auto_toggle(self, ctx, mode: bool):
        self.data = load_data()
        self.data["enabled"] = mode
        save_data(self.data)

        state = "enabled" if mode else "disabled"
        await ctx.send(f"🔧 Autoresponder is now **{state}**.")


async def setup(bot):
    await bot.add_cog(AutoResponder(bot))
