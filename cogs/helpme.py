import discord
from discord.ext import commands

class HelpMe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="helpme")
    async def helpme(self, ctx):
        """Show all commands with descriptions."""
        prefix = ","
        cogs = {}
        for command in self.bot.commands:
            if command.hidden:
                continue
            cog_name = command.cog_name or "No Category"
            if cog_name not in cogs:
                cogs[cog_name] = []
            cogs[cog_name].append(command)

        embeds = []
        for cog_name, commands_list in cogs.items():
            command_text = ""
            for cmd in commands_list:
                desc = cmd.help or "No description."
                command_text += f"**{prefix}{cmd.name}** — {desc}\n"
            embed = discord.Embed(
                title=f"📂 {cog_name} Commands",
                description=command_text[:4096],  # limit per embed
                color=discord.Color.purple()
            )
            embed.set_footer(text=f"Prefix: {prefix}")
            embeds.append(embed)

        # Send all embeds
        for embed in embeds:
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpMe(bot))
