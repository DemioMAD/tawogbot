import discord
from discord.ext.commands import CommandNotFound, CommandOnCooldown
from discord.ext import commands
from tawog import Episode
import os
import dotenv
from rich.console import Console
from datetime import datetime
from enum import Enum

dotenv.load_dotenv()
console = Console()
bot = commands.Bot(command_prefix="tawog!", intents=discord.Intents.all())
shards = set()

class LogLevels(Enum):
    SUCCESS = 1
    ERROR = 2
    INFO = 3
    WARN = 4

def log(log_level: LogLevels, message: str):
    match log_level.value:
        case 1:
            console.print(f"[bold white]{datetime.now().strftime("%H:%M:%S")}[/] [bold green]-= SUCCESS =-[/] {message}")
        case 2:
            console.print(f"[bold white]{datetime.now().strftime("%H:%M:%S")}[/] [bold red]-= ERROR =-[/] {message}")
        case 3:
            console.print(f"[bold white]{datetime.now().strftime("%H:%M:%S")}[/] [bold blue]-= INFO =-[/] {message}")
        case 4:
            console.print(f"[bold white]{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}[/] [bold yellow]-= WARNING =-[/] {message}")
        case _:
            raise ValueError("Invalid Log Level!")

@bot.event
async def on_invite_create(invite: discord.Invite):
    log(LogLevels.INFO, f"{invite.inviter} created invite {invite.code}")

@bot.event
async def on_message(message: discord.Message):
    log(LogLevels.INFO, f"{message.author} (#{message.channel.name} - {message.guild.name}): {message.content}")

    await bot.process_commands(message)

@bot.event
async def on_connect():
    log(LogLevels.INFO, "Attempting to connect to Discord's API")

@bot.event
async def on_disconnect():
    log(LogLevels.ERROR, "Bot got disconnected.")

@bot.event
async def on_shard_ready(shard_id):
    shards.add(shard_id)
    log(LogLevels.INFO, f"Shard {shard_id} is ready")
    if len(shards) == bot.shard_count:
        log(LogLevels.SUCCESS, "All shards are ready")

@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, CommandNotFound):
        log(LogLevels.ERROR, f"{ctx.command.name} was not found")
    elif isinstance(error, CommandOnCooldown):
        log(LogLevels.WARN, f"{ctx.command.name} is on cooldown. Try again after {round(error.retry_after, 2)}s.")
    else:
        log(LogLevels.ERROR, f"{type(error).__name__} - {str(error)}")

@bot.event
async def on_ready():
    log(LogLevels.SUCCESS, f"Logged in as {bot.user.name}!")

@bot.command(name="episode")
async def episode(ctx: commands.Context, *, episode_name: str):
    try:
        episode_name = episode_name.title().replace("Dvd", "DVD")
        msg = await ctx.send(f"Fetching episode info for {episode_name}...")
        episode = Episode(episode_name)
        embed = discord.Embed(
            title=episode_name,
            description=episode.info.replace("\"", "**"),
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Synopsis",
            value=episode.synopsis,
            inline=False
        )
        embed.add_field(
            name=":flag_us: U.S. air date",
            value=episode.us_airdate,
            inline=False
        )
        embed.add_field(
            name=":flag_gb: U.K. air date",
            value=episode.uk_airdate,
            inline=False
        )
        embed.set_footer(text=f"Info from {episode.url}")
        await msg.edit(content="", embed=embed)
    except Exception as e:
        await ctx.send(str(e))

bot.run(os.getenv("DISCORD_TOKEN"), log_handler=None)