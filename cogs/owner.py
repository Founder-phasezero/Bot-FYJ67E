import discord
from discord.ext import commands
import traceback
import io
import textwrap
import contextlib

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.owner_id = 1332640351499976728  # Replace with your Discord ID

    # ------------------------
    # Check if the user is owner
    # ------------------------
    def cog_check(self, ctx):
        return ctx.author.id == self.owner_id

    # ------------------------
    # Reload a cog
    # ------------------------
    @commands.command(name="reload")
    async def reload(self, ctx, cog: str):
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
            await ctx.send(f"✅ Cog `{cog}` reloaded successfully.")
        except Exception as e:
            await ctx.send(f"❌ Error reloading `{cog}`:\n```{e}```")

    # ------------------------
    # Load a cog
    # ------------------------
    @commands.command(name="load")
    async def load(self, ctx, cog: str):
        try:
            await self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"✅ Cog `{cog}` loaded successfully.")
        except Exception as e:
            await ctx.send(f"❌ Error loading `{cog}`:\n```{e}```")

    # ------------------------
    # Unload a cog
    # ------------------------
    @commands.command(name="unload")
    async def unload(self, ctx, cog: str):
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
            await ctx.send(f"✅ Cog `{cog}` unloaded successfully.")
        except Exception as e:
            await ctx.send(f"❌ Error unloading `{cog}`:\n```{e}```")

    # ------------------------
    # Shutdown bot
    # ------------------------
    @commands.command(name="shutdown")
    async def shutdown(self, ctx):
        await ctx.send("⚠️ Shutting down...")
        await self.bot.close()

    # ------------------------
    # Eval code
    # ------------------------
    @commands.command(name="eval")
    async def eval(self, ctx, *, code: str):
        env = {
            "bot": self.bot,
            "discord": discord,
            "commands": commands,
            "ctx": ctx,
        }

        code = code.strip("` ")
        stdout = io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}", env
                )
                result = await env["func"]()
        except Exception:
            value = stdout.getvalue()
            await ctx.send(f"❌ Error:\n```\n{value}{traceback.format_exc()}\n```")
        else:
            value = stdout.getvalue()
            if result is None:
                await ctx.send(f"✅ Output:\n```\n{value}\n```")
            else:
                await ctx.send(f"✅ Output:\n```\n{value}{result}\n```")

    # ------------------------
    # Send message as bot
    # ------------------------
    @commands.command(name="say")
    async def say(self, ctx, *, message: str):
        await ctx.send(message)


async def setup(bot):
    await bot.add_cog(Owner(bot))
