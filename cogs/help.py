from discord.ext import commands
import discord
from resources import checks
from resources import colours
from discord.ext.commands import cooldown, BucketType
from resources import support

class command(commands.Cog, name="help"):
    def __init__(self, client):
        self.client = client
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=["?"])
    async def help(self, ctx):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.message.add_reaction("<:CheckMark:885980150301351956>")
        try:
            channel = await ctx.message.author.create_dm()
            mariyt = await self.client.fetch_user(846298981797724161)
            await channel.send(embed=discord.Embed(title="Helpful links", description=f"""
[Commands](https://py-bot.cf/commands)
[Website](https://py-bot.cf/)
If you have any questions dm {mariyt.mention}""", color=colours.green))
        except:
            await ctx.send(embed=discord.Embed(title="Helpful links", description=f"""
[Commands](https://py-bot.cf/commands)
[Website](https://py-bot.cf/)
If you have any questions dm {mariyt.mention}""", color=colours.green), delete_after=30)


def setup(bot):
    bot.add_cog(command(bot))
