from discord.ext import commands
from discord import Embed
from datetime import datetime
from resources import colours
import asyncio
import discord
from resources import support
from discord.ext.commands import CommandNotFound
from colorama import *
from resources import errors

class command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.already_sent = False
        self.prefix = support.config.get("prefix")
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        time = datetime.utcnow()
        time = f"{time.hour:02d}:{time.minute:02d}:{time.second:02d}.{time.microsecond:06d}"
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=discord.Embed(description=f"🕰️ That command is ratelimited, try again in {error.retry_after:.2f}s.", color=colours.yellow), delete_after=10)
        elif isinstance(error, commands.CheckFailure):
            pass
        elif isinstance(error, CommandNotFound):
            cmd = str(ctx.message.content).split(self.prefix)
            cmd = cmd[1].split(" ")
            await ctx.send(embed=discord.Embed(description=f"<:QuestionMark:885978535670464533> Command `{cmd[0]}` not found.", color=colours.red), delete_after=10)
        elif isinstance(error, commands.MissingRequiredArgument):
            #help(ctx.command, _prefix)
            await ctx.send(embed=support.cmd_help(str(ctx.command), self.prefix, len(self.bot.all_commands)), delete_after=30)
        elif isinstance(error, errors.QuestionMarkError):
            await ctx.send(embed=discord.Embed(description=f"{error} cock", color=colours.red), delete_after=10)
        else:
            print(f"{Back.BLACK}{Fore.WHITE}{time}{Style.RESET_ALL} {Fore.RED}{Back.LIGHTBLACK_EX}[ERROR]{Style.RESET_ALL} {error}")
            error_ = str(error)[29:] if str(error).lower().startswith("command") else str(error)
            await ctx.send(embed=discord.Embed(description=f"<:QuestionMark:885978535670464533> {error_}", color=colours.red), delete_after=10)
            if support.config.get("debug"):
                raise error
        return

def setup(bot):
    bot.add_cog(command(bot))