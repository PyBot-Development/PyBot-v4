from discord.ext import commands
import discord
from resources import checks, support, database_driver, colours
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="op"):
    def __init__(self, client):
        self.client = client
    
    @checks.log()
    @checks.admin()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def op(self, ctx, user:discord.Member):
        await database_driver.OP_USER(user)
        await ctx.send(embed=discord.Embed(description=f"✔️ Opped user {user.mention}.", color=colours.green))
        

def setup(bot):
    bot.add_cog(command(bot))