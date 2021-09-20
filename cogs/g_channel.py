from discord.ext import commands
import discord
from resources import checks, support, GLOBAL_DATABASE, colours
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="channel"):
    def __init__(self, client):
        self.client = client
    @checks.log()
    @checks.default()
    @checks.admin()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.group()
    async def gchannel(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid sub command passed...')
    @checks.admin()
    @gchannel.group()
    async def ban(self, ctx, channel):
        channel = channel.replace("<#", "").replace(">", "")
        channel = self.client.get_channel(int(channel))
        if await GLOBAL_DATABASE.ADD_CHANNEL(channel, ctx.message.author):
            await ctx.send(embed=discord.Embed(description=f"<:CheckMark:885980150301351956> Added {channel.mention} to disabled channels.", color=colours.green))
        else:
            await ctx.send(embed=discord.Embed(description=f"<:QuestionMark:885978535670464533> Channel {channel.mention} is already in disabled channels.", color=colours.red))
    @checks.admin()
    @gchannel.group()
    async def unban(self, ctx, channel):
        channel = channel.replace("<#", "").replace(">", "")
        channel = self.client.get_channel(int(channel))
        if await GLOBAL_DATABASE.REMOVE_CHANNEL(channel):
            await ctx.send(embed=discord.Embed(description=f"<:CheckMark:885980150301351956> Removed {channel.mention} from disabled channels.", color=colours.green))
        else:
            await ctx.send(embed=discord.Embed(description=f"<:QuestionMark:885978535670464533> Channel {channel.mention} is not in disabled channels.", color=colours.red))

def setup(bot):
    bot.add_cog(command(bot))