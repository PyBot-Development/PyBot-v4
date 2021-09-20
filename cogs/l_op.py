from discord.ext import commands
import discord
from resources import checks, support, LOCAL_DATABASE, colours
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="op"):
    def __init__(self, client):
        self.client = client
    
    @checks.log()
    @checks.local_admin()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def op(self, ctx, user:discord.Member):
        await LOCAL_DATABASE.GUILD_CHECK(ctx.message.guild)
        await LOCAL_DATABASE.OP_USER(ctx.message.guild, user)
        await ctx.send(embed=discord.Embed(description=f"<:CheckMark:885980150301351956> Opped user {user.mention}.", color=colours.green))
        

def setup(bot):
    bot.add_cog(command(bot))