from discord.ext import commands
import discord
from resources import checks, support, database_driver, colours
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="cmd"):
    def __init__(self, client):
        self.client = client
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.group(aliases=["command", "cmds"])
    async def cmd(self, ctx):
        if ctx.invoked_subcommand is None:
            bdwords=""
            for item in await database_driver.GET_COMMANDS():
                bdwords += (f"`{item}`:`{await database_driver.WHO_CREATED_COMMANDS(item)}`, ")
            channel=await ctx.message.author.create_dm()
            await channel.send(embed=discord.Embed(
                title="Disabled Commands",
                description=f"{bdwords[:-2]}.",
                color=colours.blue
            ))
    @cmd.group()
    async def list(self, ctx):
        bdwords=""
        for item in await database_driver.GET_COMMANDS():
            bdwords += (f"`{item}`:`{await database_driver.WHO_CREATED_COMMANDS(item)}`, ")
        channel=await ctx.message.author.create_dm()
        await channel.send(embed=discord.Embed(
            title="Disabled Commands",
            description=f"{bdwords[:-2]}.",
            color=colours.blue
        ))
    @checks.admin()
    @cmd.group()
    async def disable(self, ctx, *, cmd):
        if cmd.lower() not in self.client.all_commands:
            await ctx.send(embed=discord.Embed(description=f"<:QuestionMark:885978535670464533> Command `{command}` does not exist.", color=colours.blue), delete_after=10)
            return
        elif await database_driver.DISABLE_COMMAND(cmd, ctx.message.author):
            await ctx.send(embed=discord.Embed(description=f"<:CheckMark:885980150301351956> Disabled `{cmd}`", color=colours.green))
        else:
            await ctx.send(embed=discord.Embed(description=f"<:QuestionMark:885978535670464533> Command `{cmd}` is already disabled.", color=colours.red), delete_after=10)
    @checks.admin()
    @cmd.group()
    async def enable(self, ctx, *, cmd):
        if cmd.lower() not in self.client.all_commands:
            await ctx.send(embed=discord.Embed(description=f"<:QuestionMark:885978535670464533> Command `{command}` does not exist.", color=colours.blue), delete_after=10)
            return
        elif await database_driver.ENABLE_COMMAND(cmd):
            await ctx.send(embed=discord.Embed(description=f"<:CheckMark:885980150301351956> Enabled `{cmd}`.", color=colours.green))
        else:
            await ctx.send(embed=discord.Embed(description=f"<:QuestionMark:885978535670464533> Command `{cmd}` is not disabled.", color=colours.red))
def setup(bot):
    bot.add_cog(command(bot))