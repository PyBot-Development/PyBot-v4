from discord.ext import commands
import discord
from resources import checks, support, colours
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="hello"):
    def __init__(self, client):
        self.client = client
    
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.group(aliases=["spam", "as"])
    async def antispam(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=discord.Embed(description=f"""Anti spam is currently `{await support.antispam()}`.""", color=colours.blue))
    @checks.admin()
    @antispam.group(aliases=["on"])
    async def enable(self, ctx):
        await support.antispam_oo(True)
        await ctx.send(embed=discord.Embed(description=f"<:CheckMark:885980150301351956> Turned Anti spam `On`.", color=colours.green))
    @checks.admin()
    @antispam.group(aliases=["off"])
    async def disable(self, ctx):
        await support.antispam_oo(False)
        await ctx.send(embed=discord.Embed(description=f"<:CheckMark:885980150301351956> Turned Anti spam `Off`.", color=colours.green))

def setup(bot):
    bot.add_cog(command(bot))