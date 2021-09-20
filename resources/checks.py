from discord.ext import commands
import discord
from datetime import datetime
from colorama import *
try: from resources import support, GLOBAL_DATABASE, LOCAL_DATABASE, colours
except: import support, GLOBAL_DATABASE, LOCAL_DATABASE, colours
import requests
import json

class guild:
    def __init__(self):
        self.id = "0000"
        self.name = "None"   
_guild = guild()
def log():
    async def _log(ctx):
        time = datetime.utcnow()
        time = f"{time.hour:02d}:{time.minute:02d}:{time.second:02d}.{time.microsecond:03d}"
        yellow = Fore.LIGHTYELLOW_EX
        green = Fore.LIGHTGREEN_EX
        reset = Style.RESET_ALL
        print(f"{Back.BLACK}{Fore.LIGHTWHITE_EX}{time}{reset}: {green}[CMD] {yellow}{ctx.message.author}{reset}: '{green}{ctx.message.content}{reset}', {yellow}Guild{reset}: {green}{ctx.message.guild}{reset}, {yellow}Channel{reset}: {green}{ctx.message.channel}{reset}")
        with open(f"logs/{support.startup_date}.log", "a+") as file:
            file.write(f"{time}: [CMD] {ctx.message.author}: '{ctx.message.content}', Guild: {ctx.message.guild}, Channel: {ctx.message.channel}\n")
        await GLOBAL_DATABASE.GET_USER(ctx.message.author)
        if support.config.get("Run-Server"):
            key = support.config.get("Server-Key")
            port = support.config.get("Server-Port")
            log = {"time": f"{time}", "author": f"{ctx.message.author}", "guild": f"{ctx.message.guild}", "channel": f"{ctx.message.channel}", "content": f"{ctx.message.content}"}
            requests.post(url=f"http://localhost:{port}/add?key={key}", data=log, json=log)
        return True
    return commands.check(_log)
def default():
    async def checks(ctx):
        guild = _guild if ctx.message.guild is None else ctx.message.guild
        await LOCAL_DATABASE.GUILD_CHECK(guild)
        await GLOBAL_DATABASE.GET_USER(ctx.message.author)
        if await GLOBAL_DATABASE.ADMIN_CHECK(ctx.message.author):
            return True
        elif await LOCAL_DATABASE.ADMIN_CHECK(guild, ctx.message.author):
            return True
        if await GLOBAL_DATABASE.CHECK_TEMPBAN(ctx.message.author) or await LOCAL_DATABASE.CHECK_TEMPBAN(guild, ctx.message.author):
            await ctx.message.add_reaction("❌")
            await ctx.send(embed=discord.Embed(description="❌ You're banned.",color=colours.red), delete_after=10)
            return False
        elif await GLOBAL_DATABASE.BANNED_CHECK(ctx.message.author) or LOCAL_DATABASE.BANNED_CHECK(guild, ctx.message.author):
            await ctx.message.add_reaction("❌")
            await ctx.send(embed=discord.Embed(description="❌ You're banned.",color=colours.red), delete_after=10)
            return False
        elif await GLOBAL_DATABASE.COMMAND_CHECK(ctx.command) or LOCAL_DATABASE.COMMAND_CHECK(guild, ctx.command):
            await ctx.message.add_reaction("❌")
            await ctx.send(embed=discord.Embed(description="❌ This command is disabled.",color=colours.red), delete_after=10)
            return False
        gbadwords = await GLOBAL_DATABASE.GET_BADWORDS()
        lbadwords = await LOCAL_DATABASE.GET_BADWORDS(guild)
        badwords = gbadwords + lbadwords
        msg = ctx.message.content
        for letter in [".", ",", ";", ":", "\\", "/", "-", "_", "​", " ", " ", " ", " ", " ", " ", " ", " ", " ", "⠀", " ", f"{support.prefix}{ctx.command}"]:
            msg = msg.replace(letter, "")
        if any(item.lower() in msg.lower() for item in badwords):
            await ctx.message.add_reaction("❌")
            await ctx.send(embed=discord.Embed(description="❌ Sorry, but some word isn't allowed here.", color=colours.blue), delete_after=10)
            return False
        elif await GLOBAL_DATABASE.CHANNEL_CHECK(ctx.message.channel) or LOCAL_DATABASE.CHANNEL_CHECK(ctx.message.guild, ctx.message.channel):
            await ctx.message.add_reaction("❌")
            channel=await ctx.message.author.create_dm()
            await channel.send(embed=discord.Embed(description=f"Channel {ctx.message.channel.mention} is not allowed. Try again in different one.", color=colours.blue))
            return False
        return True
    return commands.check(checks)

def admin():
    async def checks(ctx):
        if await GLOBAL_DATABASE.ADMIN_CHECK(ctx.message.author) or ctx.message.author.id == 846298981797724161: return True
        await ctx.send(embed=discord.Embed(description="🗝️ You've no permission.",color=colours.yellow), delete_after=10)
        return False
    return commands.check(checks)

def local_admin():
    async def checks(ctx):
        await LOCAL_DATABASE.GUILD_CHECK(ctx.message.guild)
        if await GLOBAL_DATABASE.ADMIN_CHECK(ctx.message.author) or await LOCAL_DATABASE.ADMIN_CHECK(ctx.message.guild, ctx.message.author) or ctx.message.author.id == 846298981797724161: return True
        await ctx.send(embed=discord.Embed(description="🗝️ You've no permission.",color=colours.yellow), delete_after=10)
        return False
    return commands.check(checks)