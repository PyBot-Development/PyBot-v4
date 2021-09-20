from discord.ext import commands
import discord
from resources import checks, support, LOCAL_DATABASE, colours
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="badword"):
    def __init__(self, client):
        self.client = client
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.guild_only()
    @commands.group(aliases=["badwords", "bw"])
    async def badword(self, ctx):
        LOCAL_DATABASE.GUILD_CHECK(ctx.message.guild)
        if ctx.invoked_subcommand is None:
            bdwords=""
            for item in await LOCAL_DATABASE.GET_BADWORDS(ctx.message.guild):
                bdwords += (f"`{item}`:`{await LOCAL_DATABASE.WHO_CREATED_BADWORD(ctx.message.guild, item)}`, ")
            channel=await ctx.message.author.create_dm()
            await channel.send(embed=discord.Embed(
                title="Badwords",
                description=f"{bdwords[:-2]}.",
                color=colours.blue
            ))
    @badword.group()
    async def list(self, ctx):
        bdwords=""
        for item in await LOCAL_DATABASE.GET_BADWORDS(ctx.message.guild):
            bdwords += (f"`{item}`:`{await LOCAL_DATABASE.WHO_CREATED_BADWORD(ctx.message.guild, item)}`, ")
        channel=await ctx.message.author.create_dm()
        await channel.send(embed=discord.Embed(
            title=f"{ctx.message.guild} Badwords",
            description=f"{bdwords[:-2]}.",
            color=colours.blue
        ))
    @checks.local_admin()
    @badword.group()
    async def add(self, ctx, *, word):
        if await LOCAL_DATABASE.ADD_BADWORD(ctx.message.guild, word, ctx.message.author):
            await ctx.send(embed=discord.Embed(description=f"<:CheckMark:885980150301351956> Added `{word}` to badwords.", color=colours.green))
        else:
            await ctx.send(embed=discord.Embed(description=f"❔ Word `{word}` is already in badwords.", color=colours.red))
    @checks.local_admin()
    @badword.group()
    async def remove(self, ctx, *, word):
        if await LOCAL_DATABASE.REMOVE_BADWORD(ctx.message.guild, word):
            await ctx.send(embed=discord.Embed(description=f"<:CheckMark:885980150301351956> Removed `{word}` from badwords.", color=colours.green))
        else:
            await ctx.send(embed=discord.Embed(description=f"❔ Word `{word}` is not in badwords.", color=colours.red))

def setup(bot):
    bot.add_cog(command(bot))