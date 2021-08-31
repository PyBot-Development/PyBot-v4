from discord.ext import commands
import discord
from resources import checks, support, database_driver, colours
from discord.ext.commands import cooldown, BucketType

class command(commands.Cog, name="ban"):
    def __init__(self, client):
        self.client = client
    
    @checks.log()
    @checks.admin()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def ban(self, ctx, user:discord.Member, *, reason="No Reason Specified."):
        await database_driver.BAN_USER(user, reason, ctx.message.author)
        await ctx.send(embed=discord.Embed(description=f"✔️ Banned user {user.mention}.", color=colours.green))
        try:
            channel = await user.create_dm()
            await channel.send(embed=discord.Embed(description=f"""You've been banned from using bot by {ctx.message.author.mention}.
    Reason: `{reason}`
    To: Permanent""",color=colours.blue))
        except:
            pass

def setup(bot):
    bot.add_cog(command(bot))