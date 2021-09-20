from discord.ext import commands
import discord
from resources import checks, support, GLOBAL_DATABASE, colours
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="op"):
    def __init__(self, client):
        self.client = client
    
    @checks.log()
    @checks.admin()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def gop(self, ctx, user:discord.Member):
        await GLOBAL_DATABASE.OP_USER(user)
        await ctx.send(embed=discord.Embed(description=f"<:CheckMark:885980150301351956> Opped user {user.mention}.", color=colours.green))
        

def setup(bot):
    bot.add_cog(command(bot))