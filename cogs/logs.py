from discord.ext import commands
import discord
from resources import checks
from resources import support
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="logs"):
    def __init__(self, client):
        self.client = client
    @checks.log()
    @checks.admin()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=["log"])
    async def logs(self, ctx):
        await ctx.send(file=discord.File(f"{support.path}/logs/{support.startup_date}.log"))
        

def setup(bot):
    bot.add_cog(command(bot))