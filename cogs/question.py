from discord.ext import commands
import discord
from resources import checks, support, colours
from discord.ext.commands import cooldown, BucketType
import json
import random

class command(commands.Cog, name="question"):
    def __init__(self, client):
        self.client = client
        with open(f"{support.path}/resources/questions.json") as file:
            questions = json.load(file)
        self.questions = questions
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command(aliases=["q"])
    async def question(self, ctx, times:int=1):
        if times > 30:
            await ctx.send(embed=discord.Embed(description=f"<:QuestionMark:885978535670464533> Max questions is `30`.", color=colours.red))
            return
        questions = "".join(f"\n- {random.choice(self.questions)}" for i in range(times))
        await ctx.send(embed=discord.Embed(
            description=f"{questions}",
            color=colours.green
            ))

def setup(bot):
    bot.add_cog(command(bot))
