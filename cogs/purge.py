from discord.ext import commands
import discord
from resources import checks, support, GLOBAL_DATABASE, colours
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="badword"):
    def __init__(self, client):
        self.client = client
    @checks.log()
    @checks.default()
    @checks.admin()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def purge(self, ctx, limit:int=2):
        try: await ctx.channel.purge(limit=limit)
        except: await ctx.sen(embed=discord.Embed(description="<:QuestionMark:885978535670464533> I've no permission to do that.",color=colours.red))
def setup(bot):
    bot.add_cog(command(bot))