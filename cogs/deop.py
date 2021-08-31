from discord.ext import commands
import discord
from resources import checks, support, database_driver, colours
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="deop"):
    def __init__(self, client):
        self.client = client
    
    @checks.log()
    @checks.admin()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def deop(self, ctx, user:discord.Member):
        if await database_driver.DEOP_USER(user):
            await ctx.send(embed=discord.Embed(description=f"✔️ Deopped user {user.mention}.", color=colours.green))
            return
        else:
            await ctx.send(embed=discord.Embed(description=f"❔ User {user.mention} is not opped.", color=colours.red))
            return

def setup(bot):
    bot.add_cog(command(bot))