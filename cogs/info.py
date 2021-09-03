from discord.ext import commands
import discord
from resources import checks, support, colours, database_driver
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="info"):
    def __init__(self, client):
        self.client = client
    
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def info(self, ctx):
        channel = await ctx.message.author.create_dm()
        await channel.send(embed=discord.Embed(
            title="PyBot Info",
            description=f"""
**# Versions**
Current Version: `1.2.0`.
Last Update: `03/09/2021`.
Version 1.0.0 deploy date: `31/08/2021`.

**# Github**
Initial Github reop creation date: `30/08/2021`.
Contributors: [Me](https://github.com/M2rsho)(<@846298981797724161>).

**# Bot Info**
Commands `{len(self.client.commands)}`.
Admins `{len(await database_driver.GET_ALL_ADMINS())}`.
Banned `{len(await database_driver.GET_ALL_BANNED())}`.""",
            color=colours.green
        ))

def setup(bot):
    bot.add_cog(command(bot))