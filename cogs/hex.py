from discord.ext import commands
import discord
from resources import checks, support
from discord.ext.commands import cooldown, BucketType
import random
import aiohttp
import io
from datetime import datetime

class command(commands.Cog, name="hello"):
    def __init__(self, client):
        self.client = client
    
    @checks.log()
    @checks.default()
    @cooldown(1, support.cooldown, BucketType.user)
    @commands.command()
    async def hex(self, ctx, colour="random"):
        if colour=="random": colour = '%02x%02x%02x' %  ( int(random.randint(0, 255)), int(random.randint(0, 255)), int(random.randint(0, 255)))
        try: colour_send = colour.replace("#", "")
        except:
            await ctx.send('Enter Valid Hex')
            return
        if len(colour_send) < 6:
            num = 6 - len(colour_send)
            for _ in range(num): colour_send = f"{colour_send}0"
        colour_int = int(colour_send, 16); rgb = tuple(int(colour_send[i:i+2], 16) for i in (0, 2, 4))
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'https://some-random-api.ml/canvas/colorviewer?hex={colour_send}'
            ) as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "colour.png")
                    colour = colour.replace("#", "")
                    embed = discord.Embed(title=f"Colour: #{colour}", description=f"RGB: {rgb}",color=colour_int)
                    embed.set_thumbnail(url="attachment://colour.png")
                    embed.set_footer(text=f"""Requested by: {ctx.message.author} • Today at: {datetime.utcnow().strftime("%X")} UTC""")
                    await ctx.send(embed=embed, file=file)
                else:
                    await ctx.send('Enter Valid Hex', delete_after=10)
                await session.close()

def setup(bot):
    bot.add_cog(command(bot))