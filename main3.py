import os
import asyncio
import logging
import discord
from discord.ext import commands

# ---- TOKEN ----
TOKEN = os.environ.get("DISCORD_TOKEN") or "Really man im not dumb"

# ---- logging ----
logging.basicConfig(level=logging.INFO)

# ---- intents ----
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Needed for prefix commands

# ---- Bot ----
bot = commands.Bot(command_prefix=",", intents=intents)  # Prefix is ','

# ---- events ----
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Bot is ready and using prefix commands ','.")

# ---- load cogs ----
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog_name = filename[:-3]
            try:
                await bot.load_extension(f"cogs.{cog_name}")
                print(f"Loaded cog: {cog_name}")
            except ModuleNotFoundError as e:
                print(f"Failed: {cog_name} | Missing module: {e.name}")
            except Exception as e:
                print(f"Failed: {cog_name} | {e}")

# ---- main ----
async def main():
    await load_cogs()
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
