import discord
from discord.ext import commands
import youtube_dl
import asyncio
import random
from datetime import timedelta

ytdl_format_options = {
    'format': 'bestaudio/best',
    'quiet': True,
    'extract_flat': 'in_playlist'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_queues = {}

    async def ensure_voice(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("❌ You are not in a voice channel.")
            return None
        channel = ctx.author.voice.channel
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice is None:
            voice = await channel.connect()
        elif voice.channel != channel:
            await voice.move_to(channel)
        return voice

    def add_to_queue(self, guild_id, source, title):
        if guild_id not in self.guild_queues:
            self.guild_queues[guild_id] = []
        self.guild_queues[guild_id].append({"source": source, "title": title})

    async def play_next(self, guild_id, voice):
        if self.guild_queues.get(guild_id):
            song = self.guild_queues[guild_id].pop(0)
            voice.play(
                discord.FFmpegPCMAudio(song["source"]),
                after=lambda e: asyncio.run_coroutine_threadsafe(
                    self.play_next(guild_id, voice), self.bot.loop
                )
            )
        else:
            await voice.disconnect()

    # ---------------- MUSIC COMMANDS ----------------
    @commands.command(name="play")
    async def play(self, ctx, url: str):
        voice = await self.ensure_voice(ctx)
        if not voice:
            return
        info = ytdl.extract_info(url, download=False)
        source = info['url']
        title = info.get('title', 'Unknown')
        self.add_to_queue(ctx.guild.id, source, title)
        if not voice.is_playing():
            await ctx.send(f"▶️ Now playing: {title}")
            await self.play_next(ctx.guild.id, voice)
        else:
            await ctx.send(f"➕ Added to queue: {title}")

    @commands.command(name="skip")
    async def skip(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            voice.stop()
            await ctx.send("⏭️ Skipped current song.")
        else:
            await ctx.send("❌ Nothing is playing.")

    @commands.command(name="stop")
    async def stop(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice:
            voice.stop()
            self.guild_queues[ctx.guild.id] = []
            await voice.disconnect()
            await ctx.send("⏹️ Stopped and cleared queue.")
        else:
            await ctx.send("❌ Not connected to a voice channel.")

    @commands.command(name="pause")
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            voice.pause()
            await ctx.send("⏸️ Paused music.")
        else:
            await ctx.send("❌ Nothing is playing.")

    @commands.command(name="resume")
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_paused():
            voice.resume()
            await ctx.send("▶️ Resumed music.")
        else:
            await ctx.send("❌ Nothing is paused.")

    @commands.command(name="queue")
    async def queue_cmd(self, ctx):
        queue = self.guild_queues.get(ctx.guild.id, [])
        if not queue:
            await ctx.send("📜 Queue is empty.")
        else:
            queue_titles = "\n".join([f"{i+1}. {song['title']}" for i, song in enumerate(queue)])
            await ctx.send(f"📜 Current Queue:\n{queue_titles}")

    @commands.command(name="nowplaying")
    async def nowplaying(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            await ctx.send("🎶 Currently playing audio.")
        else:
            await ctx.send("❌ Nothing is playing.")

    @commands.command(name="join")
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f"🤖 Joined {channel}")
        else:
            await ctx.send("❌ You are not in a voice channel.")

    @commands.command(name="leave")
    async def leave(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice:
            await voice.disconnect()
            await ctx.send("🤖 Left voice channel.")
        else:
            await ctx.send("❌ Not connected to a voice channel.")

    @commands.command(name="shuffle")
    async def shuffle(self, ctx):
        queue = self.guild_queues.get(ctx.guild.id, [])
        random.shuffle(queue)
        await ctx.send("🔀 Queue shuffled.")

    @commands.command(name="clearqueue")
    async def clearqueue(self, ctx):
        self.guild_queues[ctx.guild.id] = []
        await ctx.send("🗑️ Queue cleared.")

    @commands.command(name="remove")
    async def remove(self, ctx, position: int):
        queue = self.guild_queues.get(ctx.guild.id, [])
        if 0 <= position-1 < len(queue):
            removed = queue.pop(position-1)
            await ctx.send(f"🗑️ Removed song at position {position}")
        else:
            await ctx.send("❌ Invalid position.")

    @commands.command(name="fastforward")
    async def fastforward(self, ctx, seconds: int):
        await ctx.send("⏩ Fast forward not supported yet.")

    @commands.command(name="rewind")
    async def rewind(self, ctx, seconds: int):
        await ctx.send("⏪ Rewind not supported yet.")

    @commands.command(name="volume")
    async def volume(self, ctx, volume: int):
        await ctx.send("🔊 Volume control not implemented in this version.")

    @commands.command(name="seek")
    async def seek(self, ctx, seconds: int):
        await ctx.send("⏱️ Seek not implemented yet.")

    @commands.command(name="repeat")
    async def repeat(self, ctx):
        await ctx.send("🔁 Repeat not implemented yet.")

    @commands.command(name="queueinfo")
    async def queueinfo(self, ctx):
        queue = self.guild_queues.get(ctx.guild.id, [])
        await ctx.send(f"📜 Queue contains {len(queue)} songs.")

    @commands.command(name="songinfo")
    async def songinfo(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            await ctx.send("🎵 A song is currently playing.")
        else:
            await ctx.send("❌ No song is playing.")

    @commands.command(name="repeatqueue")
    async def repeatqueue(self, ctx):
        await ctx.send("🔁 Repeat queue not implemented yet.")

async def setup(bot):
    await bot.add_cog(Music(bot))
