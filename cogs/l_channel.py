from discord.ext import commands
import discord
from resources import checks, support, LOCAL_DATABASE, colours
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="channel"):
    def __init__(self, client):
        self.client = client
    @checks.log()
    @checks.default()
    @checks.local_admin()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.guild_only()
    @commands.group()
    async def channel(self, ctx):
        await LOCAL_DATABASE.GUILD_CHECK(ctx.message.guild)
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid sub command passed...')
    @checks.local_admin()
    @channel.group()
    async def ban(self, ctx, channel):
        channel = channel.replace("<#", "").replace(">", "")
        channel = self.client.get_channel(int(channel))
        if await LOCAL_DATABASE.ADD_CHANNEL(ctx.message.guild, channel, ctx.message.author):
            await ctx.send(embed=discord.Embed(description=f"<:CheckMark:885980150301351956> Added {channel.mention} to disabled channels.", color=colours.green))
        else:
            await ctx.send(embed=discord.Embed(description=f"<:QuestionMark:885978535670464533> Channel {channel.mention} is already in disabled channels.", color=colours.red))
    @checks.local_admin()
    @channel.group()
    async def unban(self, ctx, channel):
        channel = channel.replace("<#", "").replace(">", "")
        channel = self.client.get_channel(int(channel))
        if await LOCAL_DATABASE.REMOVE_CHANNEL(ctx.message.guild, channel):
            await ctx.send(embed=discord.Embed(description=f"<:CheckMark:885980150301351956> Removed {channel.mention} from disabled channels.", color=colours.green))
        else:
            await ctx.send(embed=discord.Embed(description=f"<:QuestionMark:885978535670464533> Channel {channel.mention} is not in disabled channels.", color=colours.red))

def setup(bot):
    bot.add_cog(command(bot))