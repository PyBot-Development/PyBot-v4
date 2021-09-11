from discord.ext.commands import command, Cog
from discord_components import (
    Button,
    ButtonStyle,
)
import discord
from resources import checks, support, colours, database_driver
from cogs import ban, unban, op, deop
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
    @command(aliases=["u"])
    async def user(self, ctx, user:discord.User=None):
        if user is None:
            user = ctx.message.author
        message = await ctx.send(embed=discord.Embed(description=f"User {user.mention} managment", color=colours.blue), components=[
            Button(style=ButtonStyle.red, label="Ban", custom_id="ban"), 
            Button(style=ButtonStyle.green, label="Unban", custom_id="unban"),
            Button(style=ButtonStyle.red, label="Deop", custom_id="deop"),
            Button(style=ButtonStyle.green, label="Op", custom_id="op"),
        ])
        await self.interaction_()
        while self.interaction.user.id != ctx.message.author.id:
            await self.interaction_()
        if self.interaction.custom_id == "ban":
            await ban.command.ban(self, ctx, user)
            await self.interaction.send(content=f"Done!")
        elif self.interaction.custom_id == "unban":
            await unban.command.unban(self, ctx, user)
            await self.interaction.send(content=f"Done!")
        elif self.interaction.custom_id == "op":
            await op.command.op(self, ctx, user)
            await self.interaction.send(content=f"Done!")
        elif self.interaction.custom_id == "deop":
            await deop.command.deop(self, ctx, user)
            await self.interaction.send(content=f"Done!")
        await message.delete()


def setup(bot):
    bot.add_cog(ExampleCog(bot))
