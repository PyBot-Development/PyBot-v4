from discord.ext import commands
import discord
from resources import checks, support, LOCAL_DATABASE, colours
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="unban"):
    def __init__(self, client):
        self.client = client
    
    @checks.log()
    @checks.local_admin()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def unban(self, ctx, user:discord.Member):
        await LOCAL_DATABASE.GUILD_CHECK(ctx.message.guild)
        if await LOCAL_DATABASE.UNBAN_USER(ctx.message.guild, user):
            await ctx.send(embed=discord.Embed(description=f"<:CheckMark:885980150301351956> Unbanned user {user.mention}.", color=colours.green))
            try:
                channel = await user.create_dm()
                await channel.send(embed=discord.Embed(description=f"""You've been unbanned by {ctx.message.author.mention}.
Guild: `{ctx.message.guild}`""",color=colours.blue))
            except:
                pass
        else:
            await ctx.send(embed=discord.Embed(description=f"<:QuestionMark:885978535670464533> User {user.mention} is not banned.", color=colours.red))
            return

def setup(bot):
    bot.add_cog(command(bot))