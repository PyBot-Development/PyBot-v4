from discord.ext import commands
import discord
from resources import checks, support, database_driver, colours
from discord.ext.commands import cooldown, BucketType
from datetime import datetime
class command(commands.Cog, name="data"):
    def __init__(self, client):
        self.client = client
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def data(self, ctx, *, user=None):
        if user is None:
            user = ctx.message.author
        else:
            user = await commands.UserConverter().convert(ctx, user)
        await database_driver.CHECK_TEMPBAN(user)
        r = await database_driver.GET_USER_DATA(user)
        if not not int(r[3]) != False:
            if r[7] == "Null":
                duration = "Permanent"
            else:
                utc_duration = datetime.fromtimestamp(int(r[7]))
                duration = f"<t:{int(r[7])}:f>"
            rest = f"""
Ban Reason: `{r[4]}`
Banned By: {r[5]}
Ban date: `{r[6]}`
Banned To: {duration} or `{utc_duration}` UTC
"""
        else:
            rest = ""
        await ctx.send(embed=discord.Embed(title=f"{user} Data.", description=f"""
ID: `{r[0]}`
Username: `{r[1]}`

Admin: `{not not int(r[2])}`
Banned: `{not not int(r[3])}`
{rest}
""", color=colours.blue).set_footer(text=f"""Requested by: {ctx.message.author} • Today at: {datetime.utcnow().strftime("%X")} UTC"""))
        
def setup(bot):
    bot.add_cog(command(bot))