from discord.ext import commands
import discord
from resources import checks, support, database_driver, colours
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="badword"):
    def __init__(self, client):
        self.client = client
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.group(aliases=["badwords", "bw"])
    async def badword(self, ctx):
        if ctx.invoked_subcommand is None:
            bdwords=""
            for item in await database_driver.GET_BADWORDS():
                bdwords += (f"`{item}`:`{await database_driver.WHO_CREATED_BADWORD(item)}`, ")
            channel=await ctx.message.author.create_dm()
            await channel.send(embed=discord.Embed(
                title="Badwords",
                description=f"{bdwords[:-2]}.",
                color=colours.blue
            ))
    @badword.group()
    async def list(self, ctx):
        bdwords=""
        for item in await database_driver.GET_BADWORDS():
            bdwords += (f"`{item}`:`{await database_driver.WHO_CREATED_BADWORD(item)}`, ")
        channel=await ctx.message.author.create_dm()
        await channel.send(embed=discord.Embed(
            title="Badwords",
            description=f"{bdwords[:-2]}.",
            color=colours.blue
        ))
    @checks.admin()
    @badword.group()
    async def add(self, ctx, *, word):
        if await database_driver.ADD_BADWORD(word, ctx.message.author):
            await ctx.send(embed=discord.Embed(description=f"<:CheckMark:885980150301351956> Added `{word}` to badwords.", color=colours.green))
        else:
            await ctx.send(embed=discord.Embed(description=f"❔ Word `{word}` is already in badwords.", color=colours.red))
    @checks.admin()
    @badword.group()
    async def remove(self, ctx, *, word):
        if await database_driver.REMOVE_BADWORD(word):
            await ctx.send(embed=discord.Embed(description=f"<:CheckMark:885980150301351956> Removed `{word}` from badwords.", color=colours.green))
        else:
            await ctx.send(embed=discord.Embed(description=f"❔ Word `{word}` is not in badwords.", color=colours.red))

def setup(bot):
    bot.add_cog(command(bot))