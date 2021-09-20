from discord.ext.commands import command, Cog
from discord_components import (
    Button,
    ButtonStyle,
)
import discord
from resources import checks, support, colours, GLOBAL_DATABASE
from cogs import g_ban, g_unban, g_op, g_deop
class ExampleCog(Cog):
    def __init__(self, bot):
        self.bot = bot
    async def interaction_(self):
        self.interaction = await self.bot.wait_for(
            "button_click"
            )
    @checks.admin()
    @checks.default()
    @checks.log()
    @command(aliases=["gu"])
    async def guser(self, ctx, user:discord.User=None):
        if user is None:
            user = ctx.message.author
        message = await ctx.send(embed=discord.Embed(description=f"Global User {user.mention} managment", color=colours.blue), components=[
            Button(style=ButtonStyle.red, label="Ban", custom_id="ban"), 
            Button(style=ButtonStyle.green, label="Unban", custom_id="unban"),
            Button(style=ButtonStyle.red, label="Deop", custom_id="deop"),
            Button(style=ButtonStyle.green, label="Op", custom_id="op"),
        ])
        await self.interaction_()
        while self.interaction.user.id != ctx.message.author.id:
            await self.interaction_()
        if self.interaction.custom_id == "ban":
            await g_ban.command.gban(self, ctx, user)
            await self.interaction.send(content=f"Done!")
        elif self.interaction.custom_id == "unban":
            await g_unban.command.gunban(self, ctx, user)
            await self.interaction.send(content=f"Done!")
        elif self.interaction.custom_id == "op":
            await g_op.command.gop(self, ctx, user)
            await self.interaction.send(content=f"Done!")
        elif self.interaction.custom_id == "deop":
            await g_deop.command.gdeop(self, ctx, user)
            await self.interaction.send(content=f"Done!")
        await message.delete()


def setup(bot):
    bot.add_cog(ExampleCog(bot))
