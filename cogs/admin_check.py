from discord.ext import commands
import discord
from resources import checks, support, database_driver
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="admin_check"):
    def __init__(self, client):
        self.client = client
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def admin_check(self, ctx):
        r = await database_driver.ADMIN_CHECK(ctx.message.author)
        await ctx.send(r)

def setup(bot):
    bot.add_cog(command(bot))