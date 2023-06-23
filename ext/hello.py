from discord.ext import commands

@commands.hybrid_command(brief="Says hello!", help="Says hello, nothing else.")
async def hello(ctx):
    await ctx.send("Hello!")

async def setup(bot):
    bot.add_command(hello)