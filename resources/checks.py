from discord.ext import commands
import discord
from datetime import datetime
from colorama import *
from resources import support, database_driver, colours

def log():
    async def _log(ctx):
        time = datetime.utcnow()
        time = f"{time.hour:02d}:{time.minute:02d}:{time.second:02d}.{time.microsecond:06d}"
        yellow = Fore.LIGHTYELLOW_EX
        green = Fore.LIGHTGREEN_EX
        reset = Style.RESET_ALL
        print(f"{Back.BLACK}{Fore.LIGHTWHITE_EX}{time}{reset}: {green}[CMD] {yellow}{ctx.message.author}{reset}: '{green}{ctx.message.content}{reset}', {yellow}Guild{reset}: {green}{ctx.message.guild}{reset}, {yellow}Channel{reset}: {green}{ctx.message.channel}{reset}")
        with open(f"logs/{support.startup_date}.log", "a+") as file:
            file.write(f"{time}: [CMD] {ctx.message.author}: '{ctx.message.content}', Guild: {ctx.message.guild}, Channel: {ctx.message.channel}\n")
        await database_driver.GET_USER(ctx.message.author)
        return True
    return commands.check(_log)

def default():
    async def checks(ctx):
        await database_driver.GET_USER(ctx.message.author)
        if await database_driver.ADMIN_CHECK(ctx.message.author):
            return True
        if await database_driver.CHECK_TEMPBAN(ctx.message.author):
            await ctx.message.add_reaction("❌")
            await ctx.send(embed=discord.Embed(description="❌ You're banned.",color=colours.red), delete_after=10)
            return False
        elif await database_driver.BANNED_CHECK(ctx.message.author):
            await ctx.message.add_reaction("❌")
            await ctx.send(embed=discord.Embed(description="❌ You're banned.",color=colours.red), delete_after=10)
            return False
        elif await database_driver.COMMAND_CHECK(ctx.command):
            await ctx.message.add_reaction("❌")
            await ctx.send(embed=discord.Embed(description="❌ This command is disabled.",color=colours.red), delete_after=10)
            return False
        badwords = await database_driver.GET_BADWORDS()
        msg = ctx.message.content
        for letter in [".", ",", ";", ":", "\\", "/", "-", "_", "​", " ", " ", " ", " ", " ", " ", " ", " ", " ", "⠀", " ", f"{support.prefix}{ctx.command}"]:
            msg = msg.replace(letter, "")
        if any(item.lower() in msg.lower() for item in badwords):
            await ctx.message.add_reaction("❌")
            await ctx.send(embed=discord.Embed(description="❌ Sorry, but some word isn't allowed here.", color=colours.blue), delete_after=10)
            return False
        elif await database_driver.CHANNEL_CHECK(ctx.message.channel):
            await ctx.message.add_reaction("❌")
            channel=await ctx.message.author.create_dm()
            await channel.send(embed=discord.Embed(description=f"Channel {ctx.message.channel.mention} is not allowed. Try again in different one.", color=colours.blue))
            return False
        return True
    return commands.check(checks)

def admin():
    async def checks(ctx):
        if await database_driver.ADMIN_CHECK(ctx.message.author) or ctx.message.author.id == 846298981797724161: return True
        await ctx.send(embed=discord.Embed(description="🗝️ You've no permission.",color=colours.yellow), delete_after=10)
        return False
    return commands.check(checks)