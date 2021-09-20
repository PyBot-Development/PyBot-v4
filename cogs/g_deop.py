from discord.ext import commands
import discord
from resources import checks, support, GLOBAL_DATABASE, colours
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="deop"):
    def __init__(self, client):
        self.client = client
    
    @checks.log()
    @checks.admin()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def gdeop(self, ctx, user:discord.Member):
        if await GLOBAL_DATABASE.DEOP_USER(user):
            await ctx.send(embed=discord.Embed(description=f"<:CheckMark:885980150301351956> Deopped user {user.mention}.", color=colours.green))
        else:
            await ctx.send(embed=discord.Embed(description=f"<:QuestionMark:885978535670464533> User {user.mention} is not opped.", color=colours.red))
        return

def setup(bot):
    bot.add_cog(command(bot))